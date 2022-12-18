def needs_deployment(target_release_number, rollback_release_number):
        return target_release_number > rollback_release_number