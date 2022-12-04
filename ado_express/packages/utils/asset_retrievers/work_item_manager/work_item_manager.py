from collections import defaultdict
from packages.authentication.ms_authentication.ms_authentication import MSAuthentication

class WorkItemManager:

    def __init__(self, ms_authentication: MSAuthentication):
        self.release_client = ms_authentication.client
        self.buid_client = ms_authentication.build_client
        self.work_item_tracking_client = ms_authentication.work_item_tracking_client
        self.git_client = ms_authentication.git_client

    def get_query_build_ids(self, query_id):
        build_ids = []
        query_work_items = self.get_query_work_items(query_id)

        for query_work_item in query_work_items:
            work_item = self.get_work_item(query_work_item.id)
            relations = self.get_work_item_relations(work_item)
            pull_requests = self.get_pull_requests(relations)

            for pr in pull_requests:
                merged_commit_statuses, project = self.get_statuses_from_pull_request(pr)

                if merged_commit_statuses is None: continue # No merged PRs found

                for status in merged_commit_statuses:
                    build_id = self.get_build_id_from_status(status, project) # Returns dict of deployments {'definition_name': 'build_number'}

                    if build_id is not None: build_ids.append(build_id)
        
        return build_ids

    def get_query_work_items(self, query_id):
        query_results = self.work_item_tracking_client.query_by_id(id=query_id)

        return query_results.work_items

    def get_work_item(self, work_item_id, project=None):
        work_item = self.work_item_tracking_client.get_work_item(id=work_item_id, project=project, expand='all')

        return work_item
    
    def get_work_item_relations(self, work_item, relation_name='Pull Request'):
        relations = []

        if work_item.relations:
            
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
        project = pull_request.repository.project.name

        statuses = self.git_client.get_statuses(commit_id, repository_id)

        for status in statuses:
            
            if status.state == state_key: 
                pr_commit_statuses.append(status)

        return pr_commit_statuses, project

    def get_build_id_from_status(self, status, project):
        build_id = status.target_url.split('/')[-1]

        try:
            build = self.buid_client.get_build(project, build_id)
            return build.id # Only return id if build was found
        except:
            return None # No build found (possbile error in ADO)