import os
import re
import json
import pandas as pd # type: ignore

def create_dataframe(account_data_list, dataset_type):
    dataframe = pd.DataFrame([])  # Initialize an empty DataFrame
    
    if dataset_type == "automated":
        for account_data in account_data_list:
            user_follower_count = account_data["userFollowerCount"]
            user_following_count = account_data["userFollowingCount"]
            follower_following_ratio = user_follower_count / max(1, user_following_count)
            
            temp_dataframe = pd.DataFrame([{
                "user_media_count": account_data["userMediaCount"],
                "user_follower_count": account_data["userFollowerCount"],
                "user_following_count": account_data["userFollowingCount"],
                "user_has_highligh_reels": account_data["userHasHighlighReels"],
                "user_has_external_url": account_data["userHasExternalUrl"],
                "user_tags_count": account_data["userTagsCount"],
                "follower_following_ratio": follower_following_ratio,
                "user_biography_length": account_data["userBiographyLength"],
                "username_length": account_data["usernameLength"],
                "username_digit_count": account_data["usernameDigitCount"],
                "media_comment_numbers": account_data["mediaCommentNumbers"],
                "media_comments_are_disabled": account_data["mediaCommentsAreDisabled"],
                "media_has_location_info": account_data["mediaHasLocationInfo"],
                "media_hashtag_numbers": account_data["mediaHashtagNumbers"],
                "media_like_numbers": account_data["mediaLikeNumbers"],
                "mediaUpload_times": account_data["mediaUploadTimes"],
                "automated_behaviour": account_data["automatedBehaviour"]
            }])
            dataframe = pd.concat([dataframe, temp_dataframe], ignore_index=True)
            
    elif dataset_type == "fake":
        for account_data in account_data_list:
            user_follower_count = account_data["userFollowerCount"]
            user_following_count = account_data["userFollowingCount"]
            follower_following_ratio = user_follower_count / max(1, user_following_count)
            
            temp_dataframe = pd.DataFrame([{
                "user_media_count": account_data["userMediaCount"],
                "user_follower_count": account_data["userFollowerCount"],
                "user_following_count": account_data["userFollowingCount"],
                "user_has_profil_pic": account_data["userHasProfilPic"],
                "user_is_private": account_data["userIsPrivate"],
                "follower_following_ratio": follower_following_ratio,
                "user_biography_length": account_data["userBiographyLength"],
                "username_length": account_data["usernameLength"],
                "username_digit_count": account_data["usernameDigitCount"],
                "is_fake": account_data["isFake"]
            }])
            dataframe = pd.concat([dataframe, temp_dataframe], ignore_index=True)
    
    return dataframe


def import_data(dataset_path, dataset_version):
    dataset_type = re.findall("automated|fake", dataset_version)[0]
    if dataset_type == "automated":
        with open(f"{dataset_path}/{dataset_version}/automatedAccountData.json") as json_file:
            automated_account_data = json.load(json_file)
        with open(f"{dataset_path}/{dataset_version}/nonautomatedAccountData.json") as json_file:
            nonautomated_account_data = json.load(json_file)
            
        automated_account_dataframe = pd.concat(
            [create_dataframe(automated_account_data, dataset_type)], ignore_index=True
        )
        nonautomated_account_dataframe = pd.concat(
            [create_dataframe(nonautomated_account_data, dataset_type)], ignore_index=True
        )
        merged_dataframe = pd.concat(
            [automated_account_dataframe, nonautomated_account_dataframe], ignore_index=True
        )
        data = {
            "dataset_type": dataset_type,
            "dataframe": merged_dataframe
        }
    
    elif dataset_type == "fake":
        with open(f"{dataset_path}/{dataset_version}/fakeAccountData.json") as json_file:
            fake_account_data = json.load(json_file)
        with open(f"{dataset_path}/{dataset_version}/realAccountData.json") as json_file:
            real_account_data = json.load(json_file)
            
        fake_account_dataframe = pd.concat(
            [create_dataframe(fake_account_data, dataset_type)], ignore_index=True
        )
        real_account_dataframe = pd.concat(
            [create_dataframe(real_account_data, dataset_type)], ignore_index=True
        )
        merged_dataframe = pd.concat(
            [fake_account_dataframe, real_account_dataframe], ignore_index=True
        )
        data = {
            "dataset_type": dataset_type,
            "dataframe": merged_dataframe
        }
            
    return data