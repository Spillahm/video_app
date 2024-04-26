
from django.test import TestCase
from django.urls import reverse
from .models import Video
from django.db import IntegrityError
from django.core.exceptions import ValidationError
# Create your tests here.

class TestHomePageMessage(TestCase):

    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Exercise Videos')

class TestAddVideos(TestCase):

    def test_add_video(self):

        valid_video = {
            'name': 'yoga',
            'url': 'https://www.youtube.com/watch?v=nardrbgqZ00',
            'notes': 'yoga is good for the body'
        }

        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        self.assertTemplateUsed('video_collection/video_list.html')

        #does the video show new video?
        self.assertContains(response, 'yoga')
        self.assertContains(response, 'yoga is good for the body')
        self.assertContains(response, 'https://www.youtube.com/watch?v=nardrbgqZ00')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()

        self.assertEqual( 'yoga',video.name)
        self.assertEqual('https://www.youtube.com/watch?v=nardrbgqZ00', video.url)
        self.assertEqual('yoga is good for the body', video.notes)
        self.assertEqual('nardrbgqZ00', video.video_id)


    def test_add_video_invalid_url_not_added(self):
        invalid_video_urls [
                'https://www.youtube.com/watch'
                'https://www.youtube.com/watch?'
                'https://github.com'
                'https://minneapolis.edu'


            ]

        for invalid_video_url in invalid_video_urls:

                new_video = {
                    'name':'example',
                    'url': invalid_video_url,
                    'notes':'example notes'
                }

                url = reverse('add_video')
                response = self.client.post(url, new_video)

                self.assertTemplateNotUsed('video_collection/add.html')

                messages = response.context['messages']
                message_texts = [message.message for message in messages]

                self.assertIn('invalid YouTube URL', messages)
                self.assertIn('please check the data entered.', messages)

                video_count = Video.objects.count()
                self.assertEqual(0, video_count)



class TestVideoList(TestCase):
    def test_all_videos_displayed_in_correct_order(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

        expected_video_order = [v3, v2, v4, v1]

        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_video_order)

    def test_no_video_message(self):
            url = reverse('video_list')
            response = self.client.get(url)
            self.assertContains(response, 'No videos.')
            self.assertEqual(0, len(response.context['videos']))


    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')

        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '1 video')
        self.assertNoContains(response, ' videos')

    def test_video_number_message_two_video(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')

        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '2 video')
        #self.assertNoContains(response, '2 videos')


class TestVideosSearch(TestCase):
    pass

class TestVideosModel(TestCase):

    def test_invalid_url_raises_validation_error(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch/somethingelse'
            'https://www.youtube.com/watch?'
            'https://github.com'
            'https://minneapolis.edu'

        ]

        for invalid_video_url in invalid_video_urls:

            with self.assertRaises(ValidationError):

                Video.objects.create(name='example', url=invalid_video_url, notes='example note')

        self.assertEqual(0, Video.objects.count())





    def test_duplicate_video_raises_intergrity_error(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')
        with self.assertRaises(IntegrityError):
            video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')


