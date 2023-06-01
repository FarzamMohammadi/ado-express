def needs_deployment(target_release_number, rollback_release_number):
        return int(target_release_number) > int(rollback_release_number)