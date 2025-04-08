from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta

# Add logging to debug the members field
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = [
            User(_id=ObjectId(), username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
            User(_id=ObjectId(), username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
            User(_id=ObjectId(), username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
            User(_id=ObjectId(), username='crashoverride', email='crashoverride@mhigh.edu', password='crashoverridepassword'),
            User(_id=ObjectId(), username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
        ]
        User.objects.bulk_create(users)

        # Create teams
        team1 = Team(_id=ObjectId(), name='Blue Team')
        team2 = Team(_id=ObjectId(), name='Gold Team')
        team1.save()
        team2.save()
        # Update the members field to store only user IDs as strings
        import json
        team1.members = json.dumps([str(user._id) for user in users[:2]])
        team2.members = json.dumps([str(user._id) for user in users[2:]])
        
        # Log the members field before saving
        logger.debug(f"Team1 members: {team1.members}")
        logger.debug(f"Team2 members: {team2.members}")

        team1.save()
        team2.save()

        # Update Activity creation to use user_id instead of user
        activities = [
            Activity(_id=ObjectId(), user_id=str(users[0]._id), activity_type='Cycling', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user_id=str(users[1]._id), activity_type='Crossfit', duration=timedelta(hours=2)),
            Activity(_id=ObjectId(), user_id=str(users[2]._id), activity_type='Running', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user_id=str(users[3]._id), activity_type='Strength', duration=timedelta(minutes=30)),
            Activity(_id=ObjectId(), user_id=str(users[4]._id), activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)

        # Update Leaderboard creation to use user_id instead of user
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user_id=str(users[0]._id), score=100),
            Leaderboard(_id=ObjectId(), user_id=str(users[1]._id), score=90),
            Leaderboard(_id=ObjectId(), user_id=str(users[2]._id), score=95),
            Leaderboard(_id=ObjectId(), user_id=str(users[3]._id), score=85),
            Leaderboard(_id=ObjectId(), user_id=str(users[4]._id), score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
