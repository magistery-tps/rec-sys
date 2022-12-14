#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import sys
sys.path.append('./src')
from domain_context import DomainContext
#------------------------------------------------------------------------------
#
#
#
#
#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
if __name__ == '__main__':
    ctx = DomainContext(
        host      = 'http://localhost:8000',
        temp_path = './temp'
    )
    ctx.svd_distance_matrix_job.execute()
    ctx.nmf_distance_matrix_job.execute()
    ctx.bert_item_distance_matrix_job('all-MiniLM-L6-v2').execute()
    ctx.bert_item_distance_matrix_job('all-MiniLM-L6-v2').execute()
    ctx.bert_item_distance_matrix_job('multi-qa-mpnet-base-dot-v1').execute()
    ctx.bert_item_distance_matrix_job('multi-qa-mpnet-base-dot-v1').execute()
