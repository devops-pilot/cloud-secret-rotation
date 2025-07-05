resource "aws_iam_policy" "secrets_read_only" {
  name   = "SecretsManagerReadOnly"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:ListSecrets"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "kms:Decrypt"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_user" "secret_sync_user" {
  name = "secret-sync-user"
}

resource "aws_iam_user_policy_attachment" "attach" {
  user       = aws_iam_user.secret_sync_user.name
  policy_arn = aws_iam_policy.secrets_read_only.arn
}

resource "aws_iam_access_key" "sync_user_key" {
  user = aws_iam_user.secret_sync_user.name
}
