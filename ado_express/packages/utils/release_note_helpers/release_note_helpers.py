def needs_deployment(target_release, rollback_release):
        return target_release.name.split('-')[1] > rollback_release.name.split('-')[1]