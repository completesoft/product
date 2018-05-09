from __future__ import unicode_literals
from django.db import migrations


def load_cvstatusname_from_fixture(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "cvstatusname")



def add_cv_status(apps, schema_editor):
    Person = apps.get_model("job", "Person")
    CvStatus = apps.get_model("job", "CvStatusName")
    CvState = apps.get_model("job", "CvState")
    cv_status_5 = CvStatus.objects.get(status=5)

    for person in Person.objects.all():
        print("PERSON", person)
        if not person.cvstate_set.all():
            cv_state = CvState(cv=person, status=cv_status_5)
            cv_state.save()


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_cvstatusname_from_fixture, add_cv_status),
    ]
