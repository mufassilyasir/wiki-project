from flask import Blueprint, redirect, url_for, request, render_template, flash, abort
from flask_login import current_user
from datetime import datetime

from .models import db, WikiPages, Categories,Faqs
from .utils import get_header_variables, convert_to_slug


admin = Blueprint("admin", __name__)

@admin.route('/admin', methods=['GET', 'POST'])
def index():
    name, logged_in, admin = get_header_variables()
    if current_user.is_authenticated and current_user.has_role(1):

        if request.method == "POST":

            if request.form.get('check') == "1":
                admin_only = True
            else:
                admin_only = False 
            add_wiki = WikiPages(slug=convert_to_slug(request.form.get('slug')), html=request.form.get('wiki'),
            title=request.form.get('slug'), updated_at=datetime.utcnow(), category=request.form.get('category'),
            admin_only=admin_only)
            db.session.add(add_wiki)
            db.session.commit()
            flash('Wiki page added!', category='success')
            return redirect(url_for('admin.index'))
        return render_template('/admin/index.html', name=name, logged_in=logged_in,
        admin=admin, categories=Categories.query.all())
    else:
        abort(403)

@admin.route('/admin/edit-wiki/<id>', methods=['GET', 'POST'])
def editwiki(id):
    name, logged_in, admin = get_header_variables()
    if current_user.is_authenticated and current_user.has_role(1):

        if id == "all" and request.method == "GET":
            return render_template('/admin/edit-wiki.html', name=name, logged_in=logged_in,
            admin=admin, all=True, wikipages=WikiPages.query.all())
        elif id == "all" and request.method == "POST":
            return redirect(url_for('admin.editwiki', id=request.form.get('wikipage_select')))
        
        elif request.method == "POST":
            if request.form.get('check') == "1":
                admin_only = True
            else:
                admin_only = False 
            wiki_query = WikiPages.query.filter_by(slug=id).first()
            wiki_query.slug = convert_to_slug(request.form.get('slug'))
            wiki_query.title = request.form.get('slug')
            wiki_query.html = request.form.get('wiki')
            wiki_query.category = request.form.get('category')
            wiki_query.updated_at = datetime.utcnow()
            wiki_query.admin_only = admin_only
            db.session.commit()
            flash('WikiPage edited!', category='success')
            return redirect(url_for('admin.editwiki', id=wiki_query.slug))

        return render_template('/admin/edit-wiki.html', name=name, logged_in=logged_in,
        admin=admin, all=False, wikipage=WikiPages.query.filter_by(slug=id).first_or_404(),
        categories=Categories.query.all())
    else:
        abort(403)

@admin.route('/admin/delete-wiki', methods=['GET', 'POST'])
def deletewiki():
    if current_user.is_authenticated and current_user.has_role(1):
        name, logged_in, admin = get_header_variables()

        if request.method == "POST":
            WikiPages.query.filter_by(slug=request.form.get('wikipage_select')).delete()
            db.session.commit()
            flash('WikiPage edited!', category='success')
            return redirect(url_for('admin.deletewiki'))

        return render_template('/admin/delete-wiki.html', logged_in=logged_in,
        admin=admin, name=name, wikipages=WikiPages.query.all(),
        categories=Categories.query.all())

@admin.route('/admin/categories', methods=['GET','POST'])
def categories():
    if current_user.is_authenticated and current_user.has_role(1):
        name, logged_in, admin = get_header_variables()

        if request.method == "POST":
            if request.form.get('type') == 'add':
                category = Categories(category_name=request.form.get('category'))
                db.session.add(category)
                db.session.commit()
                flash('Category added!', category='success')
                return redirect(url_for('admin.categories'))
            
            elif request.form.get('type') == 'delete':
                Categories.query.filter_by(id=request.form.get('category_id')).delete()
                db.session.commit()
                flash('Category deleted!', category='success')
                return redirect(url_for('admin.categories'))

        return render_template('/admin/categories.html', logged_in=logged_in,
            admin=admin, name=name, categories=Categories.query.all())

@admin.route('/admin/faq', methods=['GET', 'POST'])
def faq():
    if current_user.is_authenticated and current_user.has_role(1):
        name, logged_in, admin = get_header_variables()

        if request.method == "POST":
            if request.form.get('type') == 'add':
                faq = Faqs(question=request.form.get('question'),
                answer=request.form.get('answer'))
                db.session.add(faq)
                db.session.commit()
                flash('FAQ Added!', category='success')
                return redirect(url_for('admin.faq'))
            
            elif request.form.get('type') == 'delete':
                Faqs.query.filter_by(id=request.form.get('faq_select')).delete()
                db.session.commit()
                flash('FAQ Deleted!', category='success')
                return redirect(url_for('admin.faq'))

        return render_template('/admin/faq.html', logged_in=logged_in,
            admin=admin, name=name, faqs=Faqs.query.all(),
            categories=Categories.query.all())