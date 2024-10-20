from models import User,Post, db
from app import app


with app.app_context():
    # drop and create table's info
    db.drop_all()
    db.create_all()

    # if table is not empty it then it will empty
    User.query.delete()

    # Test Users 
    whis = User(first_name='Whis',last_name='Dogman')
    vamp = User(first_name='Vamp',last_name='Dogman')
    tiggy = User(first_name='Tiggy',last_name='Tigerson', image_url='https://w0.peakpx.com/wallpaper/1002/951/HD-wallpaper-jujutsu-kaisen-op-strong-anime-gojo-satoru-love.jpg')

    # add test Users
    db.session.add_all([whis,vamp,tiggy])
    # commit test User
    db.session.commit()

    post1 = Post(title = "fun",content = "dwaha0dwjowajd" , user_id = 1)
    post2 = Post(title = "kng queen",content = "njsnefoanfa" , user_id = 1)
    post3 = Post(title = "Meowers",content = "dwaoijnwodnjaojoawijowajawd" , user_id = 2)
    post4 = Post(title = "Dad",content = "d" , user_id = 3)

    # add test Posts
    db.session.add_all([post1,post2,post3,post4])
    # commit test Posts
    db.session.commit()

    print("Database seeded!")