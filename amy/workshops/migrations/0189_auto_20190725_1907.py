# Generated by Django 2.1.7 on 2019-07-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0188_WorkshopRequest_new_or_changed_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshoprequest',
            name='administrative_fee',
            field=models.CharField(choices=[('nonprofit', 'I am with a government site, university, or other nonprofit. I understand the workshop fee of US$2500, and agree to follow through on The Carpentries invoicing process.'), ('forprofit', 'I am with a corporate or for-profit site. I understand The Carpentries staff will contact me about workshop fees. I will follow through on The Carpentries invoicing process for the agreed upon fee.'), ('member', 'I am with a Member Organisation so the workshop fee does not apply (Instructor travel costs will still apply).'), ('waiver', 'I am requesting a scholarship for the workshop fee (Instructor travel costs will still apply).')], default=None, max_length=20, verbose_name='Which of the following applies to your payment for the administrative fee?'),
        ),
        migrations.AlterField(
            model_name='workshoprequest',
            name='institution_other_name',
            field=models.CharField(blank=True, default='', help_text="Please enter institution name if it's not on the list above.", max_length=255, verbose_name='If your institutional affiliation is not listed, please enter the name'),
        ),
        migrations.AlterField(
            model_name='workshoprequest',
            name='institution_restrictions',
            field=models.CharField(choices=[('no_restrictions', 'No restrictions'), ('', 'Other:')], default=None, max_length=20, verbose_name='Our instructors live, teach, and travel globally. We understand that institutions may have citizenship or other requirements for employees or volunteers who facilitate workshops. If your institution fits this description, please share your requirements or note that there are no restrictions.'),
        ),
        migrations.AlterField(
            model_name='workshoprequest',
            name='number_attendees',
            field=models.CharField(choices=[('10-40', '10-40 (one room, two instructors)'), ('40-80', '40-80 (two rooms, four instructors)'), ('80-120', '80-120 (three rooms, six instructors)')], default=None, help_text="This number doesn't need to be precise, but will help us decide how many instructors your workshop will need. Each workshop must have at least two instructors.", max_length=15, verbose_name='Anticipated number of attendees'),
        ),
        migrations.AlterField(
            model_name='workshoprequest',
            name='public_event',
            field=models.CharField(choices=[('public', 'Yes, this workshop is open to the public'), ('closed', 'No, this is a closed event'), ('', 'Other:')], default=None, help_text='Many of our workshops restrict registration to learners from the hosting institution. If your workshop will be open to registrants outside of your institution please let us know below.', max_length=20, verbose_name='Is this workshop open to the public?'),
        ),
        migrations.AlterField(
            model_name='workshoprequest',
            name='travel_expences_management',
            field=models.CharField(choices=[('booked', 'Hotel and airfare will be booked by site; ground travel and meals/incidentals will be reimbursed within 60 days.'), ('reimbursed', 'All expenses will be booked by instructors and reimbursed within 60 days.'), ('', 'Other:')], default=None, max_length=20, verbose_name='How will you manage travel expenses for Carpentries Instructors?'),
        ),
    ]
