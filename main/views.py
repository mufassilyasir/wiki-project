from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from main.models import Faqs, WikiPages, Categories, db
from main.utils import get_header_variables, convert_to_slug
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from flask_mail import Message
from . import mail
from sqlalchemy import or_

import os 

views = Blueprint("views", __name__, static_folder="static", template_folder="templates")

load_dotenv()
DIRECTORY_FOR_PROFILE_PICS = os.getenv('DIRECTORY_FOR_PROFILE_PICS')


@views.route('/')
def index():
    name, logged_in, admin = get_header_variables()
    return render_template('views/index.html', home=True, logged_in=logged_in,
    name=name, admin=admin, categories=Categories.query.all())

@views.route('/wiki/<slug>')
def wikipage(slug):
    name, logged_in, admin = get_header_variables()
    wiki = WikiPages.query.filter_by(slug=slug).first_or_404()
    if wiki.admin_only == True and admin != True:
        abort(404)


    # Parse the HTML content
    soup = BeautifulSoup(wiki.html, 'html.parser')

    # Define a mapping of H tag levels to H tag names
    htag_mapping = {
        'h1': 'h1',
        'h2': 'h2',
        'h3': 'h3',
        # Add more H tags as needed
    }

    toc = []
    updated_html = None

    # Loop through all H tags and replace them with the desired line
    for h_tag in soup.find_all(['h1', 'h2', 'h3']):


        toc.append({
            'tag': h_tag.name,
            'text': h_tag.text,
            'id': convert_to_slug(h_tag.text)
        })
        # Extract the text and ID (if available) from the H tag
        text = h_tag.text
        
        # Get the H tag name (e.g., h1, h2, h3) based on its level
        htag_level = h_tag.name
        htag_name = htag_mapping.get(htag_level, htag_level)

        # Create the replacement line with the extracted text, ID, and H tag name
        replacement_line = f'<{htag_name} class="c_head load-order-2" id="{convert_to_slug(text)}">{text}</{htag_name}>'
        # Replace the H tag with the desired line
        h_tag.replace_with(BeautifulSoup(replacement_line, 'html.parser'))

        # Get the updated HTML content
        updated_html = soup.prettify()

    

    return render_template('views/wiki-page.html', logged_in=logged_in,
    name=name, admin=admin, wiki=wiki, updated_html=updated_html, toc=toc,
    categories=Categories.query.all())


@views.route('/faq')
def faq():
    name, logged_in, admin = get_header_variables()

    return render_template('views/faq.html', logged_in=logged_in,
    name=name, admin=admin, faqs=Faqs.query.all(), faq=True, 
    categories=Categories.query.all())

@views.route('/contact-us', methods=['GET', 'POST'])
def contact():
    name, logged_in, admin = get_header_variables()


    if request.method == "POST":
        msg = Message("New Contact Us Form Message", recipients=['email'], body=f"""Full Name: {request.form.get('name')}, 
            Email: {request.form.get('email')}, Phone Number: {request.form.get('phone')}, Message: {request.form.get('message')} """)
        mail.send(msg)
        flash('Message sent!', category='success')
        return redirect(url_for('views.contact'))

    return render_template('views/contact.html', logged_in=logged_in,
    name=name, admin=admin, contact=True, 
    categories=Categories.query.all())

@views.route('/category/<id>')
def category(id):
    name, logged_in, admin = get_header_variables()

    results = WikiPages.query.filter_by(category=id).all()
    return render_template('/views/categories.html',logged_in=logged_in,
        name=name, admin=admin, categories=Categories.query.all(), results=results)

@views.route('/search', methods=['GET', 'POST'])
def search():
    name, logged_in, admin = get_header_variables()

    query = request.args.get('query')
    if query:

        if query.find('-') == -1:
            if admin == True:
                wikipage = WikiPages.query.filter((WikiPages.title==query) | (WikiPages.slug==query)).first()
            else:
                wikipage = WikiPages.query.filter(((WikiPages.title==query) | (WikiPages.slug==query)) & (WikiPages.admin_only == False)).first()

            if wikipage:
                return redirect(url_for('views.wikipage', slug=wikipage.slug))

        keywords = query.split('-')
        results = []
        for keyword in keywords:
            if admin == True:
                keyword_results = WikiPages.query.filter((or_(WikiPages.slug.like(f'%{keyword}%'), WikiPages.html.like(f'%{keyword}%')))).all()
            else:
                keyword_results = WikiPages.query.filter((or_(WikiPages.slug.like(f'%{keyword}%'), WikiPages.html.like(f'%{keyword}%'))) &  (WikiPages.admin_only == False)).all()
            
            unique_results = set(results)

            new_results = [result for result in keyword_results if result not in unique_results]

            results.extend(new_results)

        
        return render_template('/views/search.html',logged_in=logged_in,
        name=name, admin=admin, results=results,categories=Categories.query.all())
    else:
        query = convert_to_slug(request.form.get('search'))
        return redirect(url_for('views.search',query=query))