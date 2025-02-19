# ./infrastructure/variables.tf

variable "region" {
  description = "AWS 리전"
  type        = string
  default     = "ap-northeast-2"
}

variable "dynamodb_table_name" {
  description = "DynamoDB 테이블 이름"
  type        = string
  default     = "Users"
}

variable "tags" {
  description = "공통 태그"
  type = map(string)
  default = {
    Environment = "Dev"
    Team        = "DailyDevQ"
  }
}
