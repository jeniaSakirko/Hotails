import pytest
from .models import Review, DayCare, DogOwner
from django.core.validators import ValidationError


@pytest.mark.django_db()
class TestReviewModel:
    def test_persist_review(self, review, review_data):
        assert review.review == pytest.REVIEW
        assert review in Review.objects.all()

    def test_del_review(self, review):
        review.delete()
        assert review not in Review.objects.all()

    @pytest.mark.parametrize("rating", [-1, 6])
    def test_rating_limit_min(self, rating, review_data):
        with pytest.raises(ValidationError):
            Review.create(review=pytest.REVIEW, rating=rating, daycare_id=pytest.DAY_CARE_ID,
                          dogowner_id=pytest.DOG_OWNER_ID)

    def test_delete_related_daycare(self, create_daycare_user, review, review_data):
        assert create_daycare_user in DayCare.objects.all()
        assert review in Review.objects.all()

        create_daycare_user.delete()
        assert create_daycare_user not in DayCare.objects.all()
        assert review not in Review.objects.all()

    def test_delete_related_dogowner(self, create_dog_owner_user, review, review_data):
        assert create_dog_owner_user in DogOwner.objects.all()
        assert review in Review.objects.all()

        create_dog_owner_user.delete()
        assert create_dog_owner_user not in DogOwner.objects.all()
        assert review in Review.objects.all()

    @pytest.mark.parametrize("number_of_reviews", [0, 1, 3])
    def test_get_review_by_daycare_id(self, number_of_reviews, create_dog_owner_user, create_daycare_user):
        review_list = [Review.create(review='review', rating=1, daycare_id=create_daycare_user.id,
                                     dogowner_id=create_dog_owner_user.id)
                       for _ in range(number_of_reviews)]

        reviews_by_id_list = Review.get_review_by_daycare_id(create_daycare_user.id)

        assert len(reviews_by_id_list) == number_of_reviews
        for position, review in enumerate(reviews_by_id_list):
            assert review == review_list[position]
