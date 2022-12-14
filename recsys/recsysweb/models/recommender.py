from django.db          import models
from .similarity_matrix import SimilarityMatrix
from .recommender_type  import RecommenderType


class Recommender(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(
        max_length   = 200,
        verbose_name = 'Name',
        unique       = True
    )
    type        = models.IntegerField(
        choices = RecommenderType.choices,
        default = RecommenderType.COLLAVORATIVE_FILTERING
    )
    description = models.TextField(
        max_length   = 5000,
        verbose_name = 'Description',
        null         = True,
        blank        = True
    )
    user_similarity_matrix = models.ForeignKey(
        SimilarityMatrix,
        db_column    = 'user_similarity_matrix_id',
        related_name ='%(class)s_user_similarity_matrix_id',
        on_delete    = models.DO_NOTHING,
        unique       = False,
        verbose_name = 'User Similarity Matrix',
        null         = True,
        blank        = True
    )
    item_similarity_matrix = models.ForeignKey(
        SimilarityMatrix,
        db_column    = 'item_similarity_matrix_id',
        related_name ='%(class)s_item_similarity_matrix_id',
        on_delete    = models.DO_NOTHING,
        unique       = False,
        verbose_name = 'Item Similarity Matrix',
        null         = True,
        blank        = True
    )
    max_similar_users         = models.IntegerField(default = 0, verbose_name = 'Max Similar Users')
    max_items_by_similar_user = models.IntegerField(default = 0, verbose_name = 'Max Items by Similar Users')
    max_similar_items         = models.IntegerField(default = 0, verbose_name = 'Max Similar Items')
    position = models.IntegerField(default = 1, verbose_name = 'Position in Recommendations View')
    enable = models.BooleanField(default = True, verbose_name = 'Enable')


    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("info", "Show recommender debug information"),
            ("reset_interactions", "Reset User Interactions"),
        )