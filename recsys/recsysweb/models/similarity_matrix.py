from django.db               import models
from .similarity_matrix_type import SimilarityMatrixType


class SimilarityMatrix(models.Model):
    id          = models.AutoField(primary_key=True)
    type        = models.IntegerField(
        choices      = SimilarityMatrixType.choices,
        default      = SimilarityMatrixType.USER_TO_USER,
        verbose_name = 'Similarity Matrix Type'
    )
    name        = models.CharField(
        max_length   = 200,
        verbose_name = 'Name',
        unique       = True
    )
    description = models.TextField(
        max_length   = 5000,
        verbose_name = 'Description'
    )
    version     = models.IntegerField(default=0, verbose_name = 'Version')

    def __str__(self):
        return self.name
