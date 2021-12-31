from django.db import models
import uuid


class Project(models.Model):
  """プロジェクト"""

  """フィールド定義"""
  name = models.CharField(verbose_name='プロジェクト名', max_length=20)
  uuid = models.UUIDField(default=uuid.uuid4, editable=False) #プロジェクト識別番号

  def __str__(self):
      return str(self.name)



class Knowledge(models.Model):
  """得意分野"""

  """フィールド定義"""
  name = models.CharField(verbose_name='得意分野', max_length=20)

  def __str__(self):
      return str(self.name)


class Person(models.Model):
  """人物"""

  """フィールド定義"""
  name = models.CharField(verbose_name='名前', max_length=20)
  nickname = models.CharField(verbose_name='ニックネーム', max_length=20)
  mail_to = models.EmailField(verbose_name='メールアドレス', max_length=240)
  good_at = models.ManyToManyField(Knowledge, verbose_name='得意分野')
  uuid = models.UUIDField(default=uuid.uuid4, editable=False) #個人識別番号

  def __str__(self):
      return str(self.name)


class Large(models.Model):
  """大項目"""

  """フィールド定義"""
  target_project = models.ForeignKey(Project, verbose_name='対象のプロジェクト', on_delete=models.CASCADE)
  title = models.CharField(verbose_name='大項目', max_length=50)
  start = models.DateField(verbose_name='いつから')
  finish = models.DateField(verbose_name='いつまで')
  note = models.TextField(verbose_name='備考', blank=True, null=True)
  url_1 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  url_2 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  url_3 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  uuid = models.UUIDField(default=uuid.uuid4, editable=False)#大項目識別番号

  def __str__(self):
      return str(self.title)


class Middle(models.Model):
  """中項目"""

  """難易度定義"""
  easy = 1
  normal = 3
  difficult = 5
  difficulty_choices = (
    (easy, '簡単'),
    (normal, '普通'),
    (difficult, '難しい'),
  )

  """フィールド定義"""
  target_large = models.ForeignKey(Large, verbose_name='対象の大項目', on_delete=models.CASCADE)
  title = models.CharField(verbose_name='中項目', max_length=50)
  difficulty = models.IntegerField(choices=difficulty_choices, verbose_name='難易度')
  plan_to_start = models.DateField(verbose_name='着手日_計画')
  plan_to_finish = models.DateField(verbose_name='完了日_計画')
  start = models.DateField(verbose_name='着手日_実績', blank=True, null=True)
  finish = models.DateField(verbose_name='完了日_実績', blank=True, null=True)
  note = models.TextField(verbose_name='備考', blank=True, null=True)
  url_1 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  url_2 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  url_3 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  uuid = models.UUIDField(default=uuid.uuid4, editable=False)#中項目識別番号

  def __str__(self):
      return str(self.title)


class Task(models.Model):
  """実施項目"""

  """難易度定義"""
  easy = 1
  normal = 3
  difficult = 5
  difficulty_choices = (
    (easy, '簡単'),
    (normal, '普通'),
    (difficult, '難しい'),
  )

  """フィールド定義"""
  target_middle = models.ForeignKey(Middle, verbose_name='対象の中項目', on_delete=models.CASCADE)
  title = models.CharField(verbose_name='実施項目', max_length=50)
  difficulty = models.IntegerField(choices=difficulty_choices, verbose_name='難易度')
  plan_to_start = models.DateField(verbose_name='着手日_計画')
  plan_to_finish = models.DateField(verbose_name='完了日_計画')
  start = models.DateField(verbose_name='着手日_実績', blank=True, null=True)
  finish = models.DateField(verbose_name='完了日_実績', blank=True, null=True)
  note = models.TextField(verbose_name='備考', blank=True, null=True)
  url_1 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  url_2 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  url_3 = models.CharField(verbose_name='URL', max_length=255, blank=True, null=True)
  assign = models.ManyToManyField(Person, verbose_name='担当')
  uuid = models.UUIDField(default=uuid.uuid4, editable=False)#実施項目識別番号

  def __str__(self):
      return str(self.title)
