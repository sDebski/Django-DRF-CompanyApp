from django_test_migrations.contrib.unittest_case import MigratorTestCase


class UserWorkerTestForward(MigratorTestCase):
    migrate_from = ("core", "0003_auto_20240506_1430")
    migrate_to = ("core", "0004_user_worker")

    def prepare(self):
        self.old_state.clear_delayed_apps_cache()
        User = self.old_state.apps.get_model("core", "User")
        self.user_pk = User.objects.create(
            first_name="Mark",
            last_name="Wahlberg",
            email="mark@gmail.com",
        ).pk

        Worker = self.old_state.apps.get_model("company", "Worker")

        for idx in range(3):
            Worker.objects.create(
                email=f"worker{idx}@gmail.com", username=f"worker{idx}"
            )

        self.worker_pks = Worker.objects.all().values_list("pk", flat=True)

    def test_migration(self):
        self.new_state.clear_delayed_apps_cache()
        User = self.new_state.apps.get_model("core", "User")

        user = User.objects.get(pk=self.user_pk)
        self.assertTrue(user.worker)
        self.assertIn(user.worker.pk, self.worker_pks)


class UserWorkerTestBackward(UserWorkerTestForward):
    migrate_from = UserWorkerTestForward.migrate_to
    migrate_to = UserWorkerTestForward.migrate_from

    def prepare(self):
        self.old_state.clear_delayed_apps_cache()

        Worker = self.old_state.apps.get_model("company", "Worker")
        worker = Worker.objects.create(email=f"worker@gmail.com", username=f"worker")

        User = self.old_state.apps.get_model("core", "User")
        self.user_pk = User.objects.create(
            first_name="Mark",
            last_name="Wahlberg",
            email="mark@gmail.com",
            worker=worker,
        ).pk

    def test_migration(self):
        self.new_state.clear_delayed_apps_cache()
        User = self.new_state.apps.get_model("core", "User")

        user = User.objects.get(pk=self.user_pk)

        self.assertFalse(hasattr(user, "worker"))
