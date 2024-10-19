import json
from subprocess import call

from django.core.management.base import BaseCommand
from django.conf import settings

from djangofun.django_x_wow.models import Character, SimcScore


class Command(BaseCommand):
    help = """A management command that runs simulations for all wow characters"""
    def handle(self, *args, **options):
        for c in Character.objects.all():
            if (new_checksum := c.get_equipment_checksum()) != c.equipments_checksum:
                # 1. Run a new simulation
                call(['docker',
                      'run',
                      '-v',
                      '/tmp/simc:/tmp/simc',
                      'simulationcraftorg/simc:latest',
                      f'armory={c.region},{c.realm},{c.name}',
                      'report_details=0',
                      'json=/tmp/simc/result'])
                with open('/tmp/simc/result', 'r') as report:
                    report_json = json.load(report)
                    dps_score = report_json['sim']['players'][0]['collected_data']['dps']['mean']
                    SimcScore.objects.create(character=c, dps_score=dps_score)

                # 2. Update the checksum
                old_checksum = c.equipments_checksum
                c.equipments_checksum = new_checksum
                c.save()
                print(f"Character {c} checksum refreshed: {old_checksum} -> {new_checksum}")
            else:
                print(f"Character {c} checksum not refreshed: {c.equipments_checksum}")
