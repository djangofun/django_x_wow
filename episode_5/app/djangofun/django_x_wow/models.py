from django.db import models

from djangofun.blizzard_client.client import BlizzardClient


blizzard_client = BlizzardClient()


class Character(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=10)
    realm = models.CharField(max_length=255)
    equipments_checksum = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f"{self.region}: {self.realm} - {self.name}"

    def get_equipment_checksum(self):
        character_info_json = blizzard_client.get(
            f"https://{self.region.lower()}.api.blizzard.com/profile/wow/character/{self.realm.lower()}/{self.name.lower()}",
            params={"namespace": f"profile-{self.region.lower()}"},
        ).json()
        active_spec_url = character_info_json["active_spec"]["key"]["href"]
        equipment_url = character_info_json["equipment"]["href"]

        active_spec_json = blizzard_client.get(active_spec_url).json()
        equipment_json = blizzard_client.get(equipment_url).json()
        role = active_spec_json["role"]["type"]  # Looking for "DAMAGE"
        equipments_checksum = ";".join(sorted([f'{x["slot"]["type"]}-{x["item"]["id"]}' for x in equipment_json["equipped_items"]]))
        if role == "DAMAGE":
            return equipments_checksum
        return self.equipments_checksum


class SimcScore(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    dps_score = models.IntegerField()
    rating_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.character} - {self.dps_score}"
