from models import db, User, Post, Tag, PostTag
from random import choice, randint
from app import app

db.drop_all()
db.create_all()

tom = User(first_name='Tom', last_name='Anderson', image_url='https://img.buzzfeed.com/buzzfeed-static/static/2021-04/1/17/enhanced/b1791b4f8f6e/original-655-1617299042-14.jpg')
goku = User(first_name='Goku', last_name='Son', image_url='https://dragonball.guru/wp-content/uploads/2021/03/goku-profile-e1616173641804-400x400.png')
vegeta = User(first_name='Vegeta')
sasuke = User(first_name='Sasuke', last_name='Uchiha', image_url='https://static.tvtropes.org/pmwiki/pub/images/naruto_sasuke__part_ii.png')
naruto = User(first_name='Naruto', last_name='Uzumaki', image_url='https://naruto-official.com/index/char_naruto.webp')
chicken = User(first_name='Colts', last_name='Chicken', image_url='https://cdn.mos.cms.futurecdn.net/BX7vjSt8KMtcBHyisvcSPK.jpg')


p1 = Post(title='How to destroy naruto', content='When i tried to destroy him... he took my arm... then proceeded to become Hokage.... Sorry for the click bait :()', user_id=4)
p2 = Post(title='I just want my brother...', content='I just want my brother back... I wish i never acted like I hated him so much... I love him!', user_id=4)
p3 = Post(title='Hi, my name Tom!', content='I made Myspace, made a bunch of money and sold out like a genius! That Suckerberg dont know what hes doing! LOL', user_id=1)
p4 = Post(title='Training Day 5899', content='I instant transmissioned back home to check in with ChiChi and she is STILL mad at me for training and taking the boys! What if Freeza comes back?? Man it gets me excited!!! I hope he does come back.... low key...', user_id=2)
p5 = Post(title='Kakarot....', content='Im the strongest Saiyan Kakarot.. Im the prince of all saiyans and that means YOU TOO!', user_id=3)
p6 = Post(title='My eyes..', content='Man my eyes have really been hurting recently.. I went to the doctor and he asked about my eye health history........ I have no idea whos eyes I actaully have anymore, so I walked out...', user_id=4)
p7 = Post(title='Believe it!!', content='Believe it!! You can be the Hokage if you really believe it, believe it!', user_id=5)
p8 = Post(title='Bok Bok', content='Bok bok, chicken chicken, bok bok, chicken head!', user_id=6)
p9 = Post(title='Sakura.. Oh Sakura', content='If only I could tell you how much I love you, but every time I turn around theres Hinata... watching me... TF is up with her??', user_id=5)
p10 = Post(title='Anyone want to fight??', content='Man!! I been training with these weak ass sons of mine and my god... Im so happy they dont have this app.. Does anyone actaully strong want to fight?? Jiren you there?? Everytime I call it goes straight to voicemail after my 10th call in a row...', user_id=2)

t1 = Tag(name='Cool')
t2 = Tag(name='Blessed')
t3 = Tag(name='Funny')
t4 = Tag(name='Bloop')
t5 = Tag(name='Sad')
t6 = Tag(name='LFG')
t7 = Tag(name='Sorry Not Sorry')


users = [tom, goku, vegeta, sasuke, naruto, chicken]
db.session.add_all(users)
db.session.commit()

posts = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]
db.session.add_all(posts)
db.session.commit()

tags = [t1,t2,t3,t4,t5,t6,t7]
db.session.add_all(tags)
db.session.commit()

def set_tags():
    for post in posts:
        end = randint(0,4)
        for i in range(0, end):
            tag = choice(tags)
            if tag not in post.tags:
                post.tags.append(tag)

        db.session.add(post)
        db.session.commit()

set_tags()
