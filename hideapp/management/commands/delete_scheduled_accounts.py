from django.core.management.base import BaseCommand
from django.utils import timezone

from hideapp.models import CustomUser


class Command(BaseCommand):

    help = "Permanently delete customer accounts whose 7-day deletion period has expired."

    def handle(self, *args, **kwargs):

        now = timezone.now()

        # -----------------------------------------------------
        # FIND ACCOUNTS WHOSE DELETION DATE HAS ARRIVED
        # -----------------------------------------------------

        users_to_delete = CustomUser.objects.filter(
            deletion_scheduled_for__isnull=False,
            deletion_scheduled_for__lte=now
        )

        count = users_to_delete.count()

        # -----------------------------------------------------
        # DELETE USERS
        # -----------------------------------------------------

        if count > 0:

            users_to_delete.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f"{count} account(s) permanently deleted."
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    "No accounts are scheduled for deletion."
                )
            )