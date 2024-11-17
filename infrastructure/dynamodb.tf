# ./infrastructure/dynamodb.tf

resource "aws_dynamodb_table" "users_table" {
  name           = var.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST" # 온디맨드 결제
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL"
  }

  tags = var.tags

  #   # 삭제 방지 설정
  # lifecycle {
  #   prevent_destroy = true
  # }

}