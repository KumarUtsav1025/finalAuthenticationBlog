from rest_framework import serializers
from roboproject.models import Post, Comment, PostImage

class PostImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

    post= serializers.IntegerField(write_only = True)

    def create(self, validated_data):
        print(validated_data)
        post_obj = Post.objects.get(id=validated_data["post"])
        comment = Comment.objects.create(post = post_obj, commentText=validated_data["commentText"])  
        return comment


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        depth = 1
        model = Post
        fields = "__all__"

    comment  = CommentSerializer(many=True, read_only=True)
    images =  PostImageSerializers(many=True, read_only=True)

    #field to post images to database
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        post = Post.objects.create(**validated_data)

        for image in uploaded_images:
            PostImage.objects.create(post = post, image=image)

        return post
    
    

    