from packages.authentication.ms_authentication.ms_authentication import MSAuthentication

class WorkItemManager:

    def __init__(self, ms_authentication: MSAuthentication):
        self.buid_client = ms_authentication.build_client
        self.work_item_tracking_client = ms_authentication.work_item_tracking_client
        self.git_client = ms_authentication.git_client

        query_work_items = self.get_query_work_items(None)

        for query_work_item in query_work_items:
            work_item = self.get_work_item(query_work_item.id) # TODO: Send each query work item individually
            relations = self.get_work_item_relations(work_item)
            pull_requests = self.get_pull_requests(relations)

            for pr in pull_requests:
                pr_commit_statuses = self.get_statuses_from_pull_request(pr)
                if pr_commit_statuses is None: continue # No completed PRs found
                    
                for status in pr_commit_statuses:
                    builds = self.get_status_builds(status) # Returns dict of deployments {'definition_name': 'build_number'}
                    if builds is not None:
                        for key in builds:
                            print(builds[key])

    def get_query_work_items(self, query_id):
        query_id = ''
        query_results = self.work_item_tracking_client.query_by_id(id=query_id)

        return query_results.work_items

    def get_work_item(self, work_item_id, project=None):
        work_item = self.work_item_tracking_client.get_work_item(id=work_item_id, project=project, expand='all')

        return work_item
    
    def get_work_item_relations(self, work_item, relation_name='Pull Request'):
        relations = []

        for relation in work_item.relations:
            attributes_name = relation.attributes['name'] or None

            if attributes_name is not None and str(attributes_name).lower() == relation_name.lower(): relations.append(relation)
                    
        return relations

    def get_pull_requests(self, relations):
        pull_requests = []
        completed_status = 'completed'
        split_key = '%2F'

        for relation in relations:
            repository_id = relation.url.split(split_key)[1]
            pull_request_id = relation.url.split(split_key)[2]

            pull_request = self.git_client.get_pull_request(repository_id, pull_request_id)

            if pull_request.status == completed_status: pull_requests.append(pull_request) #Prevents non-complete PRs from getting checked
        
        return pull_requests
    
    def get_statuses_from_pull_request(self, pull_request):
        if pull_request.last_merge_commit is None: return None # In case where pull request commit was not merged
        
        pr_commit_statuses = []
        state_key = 'succeeded'
        commit_id = pull_request.last_merge_commit.commit_id
        repository_id = pull_request.repository.id

        statuses = self.git_client.get_statuses(commit_id, repository_id)

        for status in statuses:

            if status.state == state_key: pr_commit_statuses.append(status)

        return pr_commit_statuses
    
    def get_status_builds(self, status, project=None):
        build_id = status.target_url.split('/')[-1]
        project = "International" # TODO: Find and pass the project from previous methods
        try:
            build = self.buid_client.get_build(project, build_id)
        except:
            return # No build found (possbile error in ADO)

        definition_name = build.definition.name
        build_number = build.build_number

        return {str(definition_name).lower(): str(build_number).lower()}

