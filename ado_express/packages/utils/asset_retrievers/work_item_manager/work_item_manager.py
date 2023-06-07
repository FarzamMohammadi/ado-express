import concurrent.futures

from ado_express.packages.authentication.ms_authentication.ms_authentication import \
    MSAuthentication
from ado_express.packages.common.enums import RelationTypes


class WorkItemManager:

    def __init__(self, ms_authentication: MSAuthentication):
        self.release_client = ms_authentication.client
        self.build_client = ms_authentication.build_client
        self.work_item_tracking_client = ms_authentication.work_item_tracking_client
        self.git_client = ms_authentication.git_client
    
    def get_build_id_from_status(self, status, project):
        build_id = status.target_url.split('/')[-1]

        try:
            build = self.build_client.get_build(project, build_id)
            
            return build.id # Only return id if build was found and was actually triggered by commit build
        except:
            return None # No build found (possible error in ADO)

    def get_build_ids_from_work_item(self, query_work_item):
        build_ids = []
        work_item = self.get_work_item(query_work_item.id)
        relations = self.get_work_item_relations(work_item)

        for relation in relations:
            relation_type = relation.url.split('/')[4].lower() # Pull request or direct commit
            commit, repository = self.get_commit_from_relation(relation, relation_type)

            if commit:
                commit_statuses, project = self.get_statuses_from_commit(commit, repository)

                if commit_statuses is None: continue # No merged commits found

                for status in commit_statuses:
                    build_id = self.get_build_id_from_status(status, project) # Returns dict of deployments {<definition_name>: <build_number>}

                    if build_id is not None: build_ids.append(build_id)
                    
        return build_ids
    
    def get_commit_from_relation(self, relation, relation_type):
        completed_status = 'completed'
        split_key = '%2f' # Could be upper case F for some urls, while lower case in others
        
        repository_id = relation.url.lower().split(split_key)[1] 
        relation_item_id = relation.url.lower().split(split_key)[2]

        if relation_type == RelationTypes.COMMIT:
            commit = self.git_client.get_commit(relation_item_id, repository_id)
            repository = self.git_client.get_repository(repository_id)

            return commit, repository
        elif relation_type == RelationTypes.PULL_REQUEST_ID:
            pull_request = self.git_client.get_pull_request(repository_id, relation_item_id)

            if pull_request.last_merge_commit is not None and pull_request.status == completed_status: return pull_request.last_merge_commit, pull_request.repository  #Prevents incomplete PRs from getting checked
        
        return None, None

    def get_query_build_ids(self, query_id):
        build_ids = []
        query_work_items = self.get_query_work_items(query_id)
        # Get workitem build ids
        with concurrent.futures.ThreadPoolExecutor() as executor: # Then deploy the rest of the releases
            result_builds_id_lists = executor.map(self.get_build_ids_from_work_item, query_work_items)
            
            [build_ids.extend(build_id_list) for build_id_list in result_builds_id_lists] # Merge lists
        
        return build_ids

    def get_query_work_items(self, query_id):
        query_results = self.work_item_tracking_client.query_by_id(id=query_id)

        return query_results.work_items
    
    def get_statuses_from_commit(self, commit, repository):
        if commit is None: return None # In case where pull request commit was not merged
        
        commit_statuses = []
        state_key = 'succeeded'
        project = repository.project.name
        
        statuses = self.git_client.get_statuses(commit.commit_id, repository.id)

        for status in statuses:
            
            if status.state == state_key: 
                commit_statuses.append(status)

        return commit_statuses, project

    def get_work_item(self, work_item_id, project=None):
        work_item = self.work_item_tracking_client.get_work_item(id=work_item_id, project=project, expand='all')

        return work_item
    
    def get_work_item_relations(self, work_item, relation_names=['pull request', 'fixed in commit']):
        relations = []

        if work_item.relations:
            
            for relation in work_item.relations:
                attributes_name = relation.attributes['name'] or None

                if attributes_name is not None and str(attributes_name).lower() in relation_names: relations.append(relation)
        
        return relations