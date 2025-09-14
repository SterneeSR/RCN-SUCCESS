from django.db import migrations

def create_missing_profiles(apps, schema_editor):
    """
    Finds all User objects that don't have a related Profile and creates one.
    """
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('users', 'Profile')

    # Get IDs of users who already have a profile
    users_with_profiles = Profile.objects.values_list('user_id', flat=True)

    # Filter for users who are NOT in that list
    users_without_profiles = User.objects.exclude(id__in=users_with_profiles)

    # Create a new Profile for each of them
    for user in users_without_profiles:
        Profile.objects.create(user=user)
        print(f"Created profile for user: {user.username}")


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_address_remove_profile_phone_and_more'),
    ]

    operations = [
        migrations.RunPython(create_missing_profiles),
    ]
