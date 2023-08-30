import get_social_data
import requests
from datetime import datetime
import utils

token_tuple = get_social_data.get_tokens()
user_token = token_tuple[0]
page_token = token_tuple[1][0]['access_token']
# taken from studycat facebook page
page_id = '430901646992856'

class Facebook:
    def __init__(self, access_token, page_token, page_id):
        self.access_token = access_token 
        self.page_token = page_token # non-expiring page access token
        self.page_id = page_id # taken from studycat fb page

    def get_reels_data(self, start_date, end_date):
        '''
        fetches all available metrics for Facebook reels posts
        '''
        exp_msg = "Your IG User token has most likely expired, please replace it!"

        reel_url = f"https://graph.facebook.com/v17.0/{page_id}/video_reels"
        reel_params = {
            'fields': "post_id",
            'since': start_date,
            'until': end_date,
            'access_token': page_token
        }

        try:
            reel_res = requests.get(reel_url, params=reel_params).json()
            reel_data = reel_res.get('data', 'error with reel data')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching reel data from page id: {e}")
            return exp_msg 
           
        id_list = [entry.get('id') for entry in reel_data] # id_list = ['718104076906055', '265971266293278']
        
        
        reels_data = []
        for reel_id in id_list:
            # 1st API call: gets `description`, `updated_time`, and `id` for each reel.
            info_url = f"https://graph.facebook.com/v17.0/{reel_id}"
            try:
                reel_params = {
                    'access_token': page_token
                }
                info_res = requests.get(info_url, params=reel_params).json()
                reel_data = {
                    'Date': utils.str_to_formatted_date(info_res.get('updated_time', 'date error')),
                    'Content': utils.clean_post_content(info_res.get('description', 'description error')),
                    'Content Type': 'Reel',
                    'Platform': 'FB',
                    'Boosted': '-',
                    'Reactions': '-',
                    'Comments': '-',
                    'Shares': '-',
                    'Saves': '-',
                    'Views': '-',
                    'Reach': '-',
                    'Follower Reach': '-',
                    'Non-follower Reach': '-',
                    'Post ID': page_id+'_'+str(info_res.get('id', 'id error')),
                }
                reels_data.append(reel_data)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching reel basic data: {e}")
                return exp_msg 
            
            # 2nd API call: gets reactions, reach, views for each reel.
            insights_url = f"https://graph.facebook.com/v17.0/{reel_id}/video_insights"
            try:
                insights_params = {
                    'fields': 'values',
                    'access_token': page_token
                }
                insights_res = requests.get(insights_url, params=insights_params).json()
                insights_data = insights_res.get('data', 'reel insights data err')

                desired_metrics = ["post_video_likes_by_reaction_type", "post_impressions_unique", "blue_reels_play_count"]
                
                metric_values = {}
                for entry in insights_data:
                    for metric in desired_metrics:
                        if metric in entry["id"]:
                            if metric == "post_video_likes_by_reaction_type":
                                value = entry["values"][0]["value"]["REACTION_LIKE"]
                                metric_values['Reactions'] = value
                                break
                            else:
                                value = entry["values"][0]["value"]
                                if metric == "post_impressions_unique":
                                    metric_values['Reach'] = value
                                elif metric == "blue_reels_play_count": 
                                    metric_values['Views'] = value
                                break  # to avoid duplicates
                
                for key in metric_values:
                    if key in reel_data:
                        reel_data[key] = metric_values[key]
    
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching reel insights data: {e}")
                return exp_msg 
        
        return reels_data

    ######## FOR POST TYPES OTHER THAN REELS ############
    def get_basic_data(self, start_date, end_date):
        '''
        fetches the following metrics from all fb page posts except reels specified by start_date
        and end_date: Date, Content, Content Type, Reactions, Comments, Shares. 

        Args:
        page_id: str: The unique ID of the Facebook page
        start_date: str: The start date of the posts to be fetched in the format 'MM/DD/YYYY'
        end_date: str: The end date of the posts to be fetched in the format 'MM/DD/YYYY' (non-inclusive)

        Returns:
        posts_data: A list of dictionaries containing the post data
        '''
        # convert dates
        start_date = utils.str_to_datetime(start_date)
        end_date = utils.str_to_datetime(end_date)
        
        # first we get the posts IDs of all posts (except reels) within start/end dates
        post_url = f"https://graph.facebook.com/v17.0/{self.page_id}/posts"
        post_params = {
            'fields': "post_id,created_time,message,attachments{media_type},reactions.summary(true),comments.summary(true),shares",
            'since': start_date,
            'until': end_date,
            'access_token': page_token
        }
        
        try:
            res = requests.get(post_url, params=post_params).json()
            res_data = res.get('data', 'data for res was empty')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching posts: {e}")
            exp_msg = "Your IG User token has most likely expired, please replace it!"
            return exp_msg    

        posts_data = []
        for post in res_data:
            post_data = {
                'Post ID': post['id'],
                'Date': datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d/%Y'),
                'Content': utils.clean_post_content(post.get('message', '')),
                'Content Type': post.get('attachments', {}).get('data', [{}])[0].get('media_type', '').title(),
                'Reactions': post.get('reactions', {}).get('summary', {}).get('total_count', 0),
                'Comments': post.get('comments', {}).get('summary', {}).get('total_count', 0),
                'Shares': post.get('shares', {}).get('count', 0)
            }
            posts_data.append(post_data)

        return posts_data
    
    def get_insight_data(self, start_date, end_date):
        '''
        fetches the following metrics from all fb page posts (excluding reels), 
        specified by start_date & end_date (non-inclusive): 
        Saves, Views, Reach, Follower Reach, NonFollower Reach.
        '''
        start_date = utils.str_to_datetime(start_date)
        end_date = utils.str_to_datetime(end_date)

         # First we need to produce JSON of all posts within specified date parameters
        feed_url = f"https://graph.facebook.com/v17.0/{self.page_id}/feed"
        feed_params = {
            'since': start_date,
            'until': end_date,
            'access_token': page_token
        }
        try: 
            feed_res = requests.get(feed_url, params=feed_params).json()
        except requests.exceptions.RequestException as e: 
            raise RuntimeError(f'An error occurred while fetching posts: {e}')

        # Loop through feed_res object, get all the post IDs (format: {page_id}_{post_id})
        post_id_list = [post['id'] for post in feed_res['data']]
        post_metrics = {}
        
        # Make a second API request for each post_id
        insights_params = {
            # fields: boosted, views, reach, follower reach, nonfollower reach
            "metric": "post_impressions, post_impressions_fan, post_impressions_paid, post_video_views",
            "access_token": page_token,
            "since": start_date.timestamp(),
            "until": end_date.timestamp(),
        }
    
        for post_id in post_id_list:
            # make entry in post_metrics dict
            if post_id not in post_metrics:
                post_metrics[post_id] = {}
            
            insights_url = f"https://graph.facebook.com/v17.0/{post_id}/insights"
            try:
                insights_res = requests.get(insights_url, params=insights_params).json()

                for metric_data in insights_res['data']:
                    metric_name = metric_data['name']
                    metric_value = metric_data['values'][0]['value']

                    post_metrics[post_id][metric_name] = metric_value

            except requests.exceptions.RequestException as e:
                raise RuntimeError(f'An error occurred while fetching metrics: {e}')
            
        # Now do cleanup for final insight dictionary 
        def is_boosted(post_data):
            return post_data['post_impressions_paid'] == 1
        
        insights_data = []

        for post_id, post_data in post_metrics.items():
            insight_data = {
                'Post ID': post_id,
                'Boosted': is_boosted(post_data),
                'Saves': '-',
                'Views': post_data.get('post_video_views', '-'),  
                'Reach': post_data.get('post_impressions', '-'),
                'Follower Reach': post_data.get('post_impressions_fan', '-'),
                'Non-Follower Reach': (post_data.get('post_impressions', 0) - post_data.get('post_impressions_fan', 0)) if (post_data.get('post_impressions', '-') != '-' and post_data.get('post_impressions_fan', '-') != '-') else '-'
            }
            insights_data.append(insight_data)


        return insights_data
    
    def get_combined_data(self, start_date, end_date):
        '''
        Combines basic post data and insight data from Facebook page posts within a specified date range.
        Also reorders attributes. 

        Returns:
        list: A list of dictionaries containing combined post data and insight data.
        '''
        basic_data = self.get_basic_data(start_date, end_date)
        insight_data = self.get_insight_data(start_date, end_date)

        combined_data = {}

        for basic_entry in basic_data:
            post_id = basic_entry['Post ID']
            combined_data[post_id] = basic_entry

        for insight_entry in insight_data:
            post_id = insight_entry['Post ID']
            if post_id in combined_data:
                combined_data[post_id].update(insight_entry)

        combined_list = list(combined_data.values())

        # Now we have to reorder the attributes to match those in the Google Sheet
        # Also cleans post content
        reordered_list = []
        for entry in combined_list:
            content = entry['Content']
            truncated_content = utils.clean_post_content(content)
            reordered_entry = {
                'Date': entry['Date'],
                'Content': truncated_content,
                'Content Type': entry['Content Type'].title(),
                'Platform': 'FB',
                'Boosted': entry['Boosted'],
                'Reactions': entry['Reactions'],
                'Comments': entry['Comments'],
                'Shares': entry['Shares'],
                'Saves': entry['Saves'],
                'Views': entry['Views'],
                'Reach': entry['Reach'],
                'Follower Reach': entry['Follower Reach'],
                'Non-follower Reach': entry['Non-Follower Reach'],
                'Post ID': entry['Post ID']
            }
            reordered_list.append(reordered_entry)

        return reordered_list
         
    def update_video_views(self, combined_data, start_date, end_date):
        '''
        Note: there is a distinction between post ID and video ID.
        Using post content type from insights_data, updates views of a video
        using a different endpoint. 
        '''
        # convert dates
        start_date = utils.str_to_datetime(start_date)
        end_date = utils.str_to_datetime(end_date)
        
        # first we get the video IDs of all video posts within start/end dates
        post_url = f"https://graph.facebook.com/v17.0/{self.page_id}/videos"
        post_params = {
            'fields': 'post_id, permalink_url, description',
            'since': start_date,
            'until': end_date,
            'access_token': page_token
        }
        
        # 1st API call: get video IDs (this includes both reels and videos)
        try:
            res = requests.get(post_url, params=post_params).json()
            res_data = res.get('data', 'data for video res was empty')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching posts: {e}")
            exp_msg = "Your IG User token has most likely expired, please replace it!"
            return exp_msg    
        
        # 2nd API call: isolate video IDs
        video_id_list = [entry['id'] for entry in res_data if 'videos' in entry['permalink_url']]
        # print(video_id_list) ['6797024150348728', '659662992760124']
        video_metrics = []
    

        for video_id in video_id_list:
            vid_url = f"https://graph.facebook.com/v17.0/{video_id}"
            vid_params = {
                'fields': 'description, video_insights',
                'access_token': page_token}

            try:
                vid_res = requests.get(vid_url, params=vid_params).json()
                # vid_data = vid_res.get('data', 'error with vid data')
                # print('vid data: '+ vid_data)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching video id data from page id: {e}")
                return exp_msg 
            
            if vid_res['video_insights']['data'][0]['name'] == 'total_video_views':
                video_metric = {
                    'Post Content': vid_res['description']
                }
                video_metric['Views'] = vid_res['video_insights']['data'][0]['values'][0]['value']
                video_metrics.append(video_metric)

        # Now we update the video entries in insight_data with the right view count
        for data in combined_data:
            for video in video_metrics:
                if data['Content'][:-3] in video['Post Content']:
                    data['Views'] = video['Views']


        return combined_data
    
    def get_final_data(self, start_date, end_date):
        '''
        Sorts through the combined data, which now has the right views for videos,
        to update metrics for Facebook reels. 
        '''
        main_data = self.get_combined_data(start_date, end_date)
        updated_data = self.update_video_views(main_data, start_date, end_date)
        reels_data = self.get_reels_data(start_date, end_date)

        final_data = updated_data.copy()
        final_data.extend(reels_data)

        return final_data


### TESTING ###########
# startdate = '08/02/2023'
# enddate = '08/13/2023'
# fbtest = Facebook(get_social_data.get_fb_access_token(), page_token, page_id)
# fbtest_basic_data = fbtest.get_basic_data(startdate, enddate)
# fbtest_reels_data = fbtest.get_reels_data(startdate, enddate)
# fbtest_insight_data = fbtest.get_insight_data(startdate, enddate)
# fbtest_combined_data = fbtest.get_combined_data(startdate, enddate)
# fbtest_update_video = fbtest.update_video_views(fbtest_combined_data, '08/02/2023', '08/13/2023')
# fbtest_final_data = fbtest.get_final_data(startdate, enddate)





