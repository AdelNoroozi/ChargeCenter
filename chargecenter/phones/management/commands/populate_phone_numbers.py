from django.core.management.base import BaseCommand

from chargecenter.phones.factories import PhoneNumberFactory


class Command(BaseCommand):
    help = 'Populate the database with mock phone numbers'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='The number of phone numbers to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        for _ in range(count):
            PhoneNumberFactory.create()
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} phone numbers'))
