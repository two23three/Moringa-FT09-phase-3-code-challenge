from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database
    create_tables()

    # Get user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    #check if the author is already in the database
    cursor.execute('SELECT id FROM authors WHERE name = ?', (author_name,))
    
    author_information = cursor.fetchone()

    
    if author_information:
        author_id = author_information[0]
   # Insert the author into the database or get the existing one
    else:
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
        author_id = cursor.lastrowid

    # Insert the magazine into the database or get the existing one
    cursor.execute('SELECT id FROM magazines WHERE name = ?', (magazine_name,))
    magazine_info = cursor.fetchone()

    if magazine_info:
        magazine_id = magazine_info[0]
    
    else:
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
        magazine_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # Create an article
    article = Article(None, article_title, article_content, author_id, magazine_id)

    #call the show_all function
    show_all()

def show_all():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch authors from db
    cursor.execute('SELECT * FROM authors LIMIT 5')
    authors = cursor.fetchall()

    # Fetch articles from db
    cursor.execute('SELECT * FROM articles LIMIT 5')
    articles = cursor.fetchall()

    # Fetch magazines from db
    cursor.execute('SELECT * FROM magazines LIMIT 5')
    magazines = cursor.fetchall()

    conn.close()

    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    # Display the authors
    print("\nAuthors:")
    for author in authors:
        print(Author(author["id"], author["name"]))

    # Display the articles
    print("\nArticles:")
    for article in articles:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

    
 

if __name__ == "__main__":
    main()
