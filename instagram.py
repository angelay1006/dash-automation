import requests
from datetime import datetime
import utils
import get_social_data

ig_user_id = '17841403777844964'
ig_access_token = get_social_data.get_ig_access_token()


class Instagram:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_basic_data(self, user_id, start_date, end_date):
        '''
        Meta's API convention: end_date is non-inclusive
        '''
        # convert dates
        start_date = utils.str_to_datetime(start_date)
        end_date = utils.str_to_datetime(end_date)
        base_url = f"https://graph.facebook.com/v17.0/{user_id}/media"
        
        params = {
            'fields': 'id,timestamp,caption,media_type,media_product_type,like_count,comments_count',
            'since': start_date,
            'until': end_date,
            'access_token': self.access_token
        }

        def feedvideo_or_reel(post):
            '''
            Given a post (dict), decides whether its a reel or simply a feed video.
            Only called when `media_type` is `video`. 
            '''
            if post.get('media_product_type') == 'FEED':
                return 'VIDEO'
            elif post.get('media_product_type') == 'REELS':
                return 'REEL'
            else:
                return 'feedvideo_or_reel_err'
        
        try:
            res = requests.get(base_url, params=params).json()
            res_data = res.get('data', [])

            posts_data = []
            for post in res_data:
                post_data = {
                    'Date': datetime.strptime(post['timestamp'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d/%Y'),
                    'Content': utils.clean_post_content(post['caption']),
                    'Content Type': feedvideo_or_reel(post) if post.get('media_type') == 'VIDEO' else post.get('media_type'),
                    'Platform': 'IG',
                    'Boosted': 'TRUE' if post.get('media_product_type') == 'AD' else 'FALSE',
                    'Reactions': post.get('like_count'),
                    'Comments': post.get('comments_count'),
                    'Post ID': post['id']
                }
                posts_data.append(post_data)

            return posts_data

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching posts: {e}")
            exp_msg = "Your IG User token has most likely expired, please replace it!"
            return exp_msg
    
    def handle_image(self, entry):
        '''
        Given a Post ID, uses API to get insights.
        Returns a dict of the new insights
        '''
        media_id = entry.get('Post ID')
        base_url = f"https://graph.facebook.com/v17.0/{media_id}/insights"
        params = {
                'metric': 'shares,saved,impressions,reach',
                'access_token': self.access_token
                } 
        
        insights_dict = {
                    'Shares': 0,
                    'Saves': 0,
                    'Views': 0,
                    'Reach': 0,
                    'Post ID': media_id
        }

        try:
            res = requests.get(base_url, params=params).json()
            res_data = res.get('data', 'handle_image:access token expired?')

            for metric_data in res_data:
                metric_name = metric_data.get('name')
                metric_value = metric_data['values'][0]['value']

                # Map metric name to corresponding key in insights_dict
                if metric_name == 'shares':
                    insights_dict['Shares'] = metric_value
                elif metric_name == 'saved':
                    insights_dict['Saves'] = metric_value
                elif metric_name == 'impressions':
                    insights_dict['Views'] = metric_value
                elif metric_name == 'reach':
                    insights_dict['Reach'] = metric_value
    
        except requests.exceptions.RequestException as e:
            return e
    
        return insights_dict

    def handle_video(self, entry):
        media_id = entry.get('Post ID')
        base_url = f"https://graph.facebook.com/v17.0/{media_id}/insights"
        params = {
                'metric': 'shares,saved,video_views,reach',
                'access_token': self.access_token
                } 
        
        insights_dict = {
                    'Shares': 0,
                    'Saves': 0,
                    'Views': 0,
                    'Reach': 0,
                    'Post ID': media_id
        } 

        try:
            res = requests.get(base_url, params=params).json()
            res_data = res.get('data', 'handle_video:access token expired?')

            for metric_data in res_data:
                metric_name = metric_data.get('name')
                metric_value = metric_data['values'][0]['value']

                # Map metric name to corresponding key in insights_dict
                if metric_name == 'shares':
                    insights_dict['Shares'] = metric_value
                elif metric_name == 'saved':
                    insights_dict['Saves'] = metric_value
                elif metric_name == 'video_views':
                    insights_dict['Views'] = metric_value
                elif metric_name == 'reach':
                    insights_dict['Reach'] = metric_value
    
        except requests.exceptions.RequestException as e:
            return e
    
        return insights_dict

    def handle_reel(self,entry):
        media_id = entry.get('Post ID')
        base_url = f"https://graph.facebook.com/v17.0/{media_id}/insights"
        params = {
                'metric': 'shares,saved,plays,reach',
                'access_token': self.access_token
                } 
        insights_dict = {
            'Shares': 0,
            'Saves': 0,
            'Views': 0,
            'Reach': 0,
            'Post ID': media_id
        }

        try:
            res = requests.get(base_url, params=params).json()
            res_data = res.get('data', 'handle_reels:access token expired?')

            for metric_data in res_data:
                metric_name = metric_data.get('name')
                metric_value = metric_data['values'][0]['value']

                # Map metric name to corresponding key in insights_dict
                if metric_name == 'shares':
                    insights_dict['Shares'] = metric_value
                elif metric_name == 'saved':
                    insights_dict['Saves'] = metric_value
                elif metric_name == 'plays':
                    insights_dict['Views'] = metric_value
                elif metric_name == 'reach':
                    insights_dict['Reach'] = metric_value
    
        except requests.exceptions.RequestException as e:
            return e
    
        return insights_dict

    def handle_album(self,entry):
        '''
        `shares` metric is incompatible with carousel album type
        '''
        media_id = entry.get('Post ID')
        base_url = f"https://graph.facebook.com/v17.0/{media_id}/insights"
        params = {
                'metric': 'carousel_album_saved,carousel_album_impressions,carousel_album_reach',
                'access_token': self.access_token
                } 
        insights_dict = {
            'Shares': '-',
            'Saves': 0,
            'Views': 0,
            'Reach': 0,
            'Post ID': media_id
        }

        try:
            res = requests.get(base_url, params=params).json()
            res_data = res.get('data', 'handle_reels:access token expired?')

            for metric_data in res_data:
                metric_name = metric_data.get('name')
                metric_value = metric_data['values'][0]['value']

                # Map metric name to corresponding key in insights_dict
                if metric_name == 'carousel_album_saved':
                    insights_dict['Saves'] = metric_value
                elif metric_name == 'carousel_album_impressions':
                    insights_dict['Views'] = metric_value
                elif metric_name == 'carousel_album_reach':
                    insights_dict['Reach'] = metric_value
    
        except requests.exceptions.RequestException as e:
            return e
    
        return insights_dict
    
    # We need: Shares	Saves	Views	Reach	Follower Reach	Non-follower reach
    def get_insight_data(self, basic_data):
        # we use each post ID in basic_data to query API for data
        # conditions depend on the media type of the post. 
        # this means we HAVE to call get_basic_data and pass the result in here
        '''
        unfortunately the Instagram API won't let us get follower/nonfollower reach
        to specify date parameters, must call basic_data w/ start/end date
        '''
        type_handlers = {
            'IMAGE': self.handle_image,
            'VIDEO': self.handle_video,
            'REEL': self.handle_reel,
            'CAROUSEL_ALBUM': self.handle_album
        }

        insights_lst = []

        for entry in basic_data:
            content_type = entry.get('Content Type')
            post_id = entry.get('Post ID')
            if content_type in type_handlers:
                entry_insights = type_handlers[content_type](entry)
            else:
                print("insight handler error: content type not found")
            insights_lst.append(entry_insights)
        
        return insights_lst

    def get_combined_data(self, start_date, end_date):
        '''
        Combine s basic post data and insight data from Instagram page posts within a specified date range.
        '''
        basic_data = self.get_basic_data(ig_user_id, start_date, end_date)
        insight_data = self.get_insight_data(basic_data)

        combined_data = {}

        for basic_entry in basic_data:
            post_id = basic_entry['Post ID']
            combined_data[post_id] = basic_entry
        
        for insight_entry in insight_data:
            post_id = insight_entry['Post ID']
            if post_id in combined_data:
                combined_data[post_id].update(insight_entry)

        combined_list = list(combined_data.values())
        
        # Cleaning up combined_list 
        reordered_list = [] 
        for entry in combined_list:
            reordered_entry = {
                'Date': entry['Date'],
                'Content': entry['Content'],
                'Content Type': entry['Content Type'].title(),
                'Platform': 'IG',
                'Boosted': entry['Boosted'],
                'Reactions': entry['Reactions'],
                'Comments': entry['Comments'],
                'Shares': entry['Shares'],
                'Saves': entry['Saves'],
                'Views': entry['Views'],
                'Reach': entry['Reach'],
                'Follower Reach': '-',
                'Non-follower Reach': '-',
                'Post ID': entry['Post ID']
            }
            reordered_list.append(reordered_entry)

        return reordered_list


test = Instagram(get_social_data.get_ig_access_token())
test_basic_data = test.get_basic_data(ig_user_id,'08/04/2023','08/14/2023')
# print(test.get_reels(ig_user_id,'08/18/2023','08/24/2023', test_data))
# print(test_data)
# entry = {'Date': '08/04/2023', 'Content': 'Memory, Meaning & The Benefits of Overlearning 🧠At the VUS TESOL Conference in Vietnam, ou...', 'Content Type': 'CAROUSEL_ALBUM', 'Platform': 'IG', 'Boosted': 'FALSE', 'Reactions': 13, 'Comments': 0, 'Post ID': '18006734743892699'}
# print(test.handle_album(entry))
print(test.get_combined_data('08/04/2023', '08/14/2023')) # format: [{1:2}, {3:4}, {5:6}]