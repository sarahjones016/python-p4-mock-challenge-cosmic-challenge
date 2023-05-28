from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Planet, Scientist, Mission

fake = Faker()

if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Planet.query.delete()
        Scientist.query.delete()
        Mission.query.delete()

        moon = Planet(name="Moon", distance_from_earth=238900, nearest_star="trinary star Alpha Centauri", image="https://images.theconversation.com/files/397026/original/file-20210426-23-dhor35.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1200&h=1200.0&fit=crop")
        db.session.add(moon)
        db.session.commit()
        saturn = Planet(name="Saturn", distance_from_earth=907520000, nearest_star="Proxima Centauri", image="https://solarsystem.nasa.gov/system/stellar_items/image_files/38_saturn_1600x900.jpg")
        db.session.add(saturn)
        db.session.commit()

        neil_armstrong = Scientist(name="Neil Armstrong", field_of_study="Astronaut", avatar="https://cdn.britannica.com/92/118692-050-194A0468/Neil-Armstrong-Apollo-11-Michael-Collins-Edwin.jpg")
        db.session.add(neil_armstrong)
        db.session.commit()
        buzz_aldrin = Scientist(name="Buzz Aldrin", field_of_study="Astronaut", avatar="https://media4.s-nbcnews.com/i/MSNBC/Components/Photo/_new/091002-buzzandbuzz-hmed.jpg")
        db.session.add(buzz_aldrin)
        db.session.commit()

        mission1 = Mission(name="Mission 1", scientist_id=1, planet_id=1)
        db.session.add(mission1)
        db.session.commit()
        mission2 = Mission(name="Mission 2", scientist_id=2, planet_id=2)
        db.session.add(mission2)
        db.session.commit()

        print("Done seeding!")
