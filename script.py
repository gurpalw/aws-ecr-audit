import boto3

client = boto3.client('ecr', region_name='eu-west-1')
paginator = client.get_paginator('describe_repositories')
response_iterator = paginator.paginate()
repoNames = []
maxResults = 1000

for page in response_iterator:
    for repo in page['repositories']:  # Iterate over every dict element of the list of dict.
        repoNames.append(repo['repositoryName'])  # Add the repo name to a list so we can iterate over them later.

    repoNames.sort()  # Sort alphabetically.
    print("Total Number of ECR repositories: " + str(len(repoNames)))

for repo in repoNames:  # Iterate over every repo we found earlier, and call list_images from boto3.
    images = client.list_images(repositoryName=repo, maxResults=maxResults)  # List the images for a repo.
    imagesCount = []
    imagesCount.append((len(images['imageIds'])))  # add the number of images in the repo to a list.

    # Check to see if the count is greater than the maximum allowed to be returned in one call, if it is,
    # make another call with the nextToken
    while len(images['imageIds']) == maxResults:
        images = client.list_images(repositoryName=repo, maxResults=1000, nextToken=images['nextToken'])
        imagesCount.append((len(images['imageIds'])))  # add the number of images in the repo to the list.

    print(repo + ": " + str(sum(imagesCount)))
