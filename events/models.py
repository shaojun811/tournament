from django.db import models

# 新增：赛事类型表（独立维护）
class EventType(models.Model):
    name = models.CharField('类型名称', max_length=100, unique=True)  # 如 “男子双打”、“女子双打”
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '赛事类型'
        verbose_name_plural = '赛事类型'
        ordering = ['name']

class Event(models.Model):
    name = models.CharField('赛事名称', max_length=200)
    event_type = models.ForeignKey(  # ← 改成 ForeignKey
        EventType,
        on_delete=models.PROTECT,  # 防止删除类型时误删赛事
        related_name='events',
        verbose_name='赛事类型'
    )
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    location = models.CharField('举办地点', max_length=200)
    description = models.TextField('赛事简介', blank=True)
    status = models.CharField('状态', max_length=20, choices=[
        ('upcoming', '即将举行'),
        ('ongoing', '进行中'),
        ('finished', '已结束'),
    ], default='upcoming')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_time']
        verbose_name = '赛事'
        verbose_name_plural = '赛事'


class Player(models.Model):
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]

    LEVEL_CHOICES = [
        ('2.0', '2.0'),
        ('2.5', '2.5'),
        ('3.0', '3.0'),
        ('3.5', '3.5'),
        ('4.0', '4.0'),
        ('4.5', '4.5'),
        ('5.0', '5.0+'),
    ]

    name = models.CharField('姓名', max_length=50, unique=True)
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES)
    level = models.CharField('技术水平', max_length=10, choices=LEVEL_CHOICES, default='3.5')
    created_at = models.DateTimeField('注册时间', auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.level} - {self.get_gender_display()})"

    class Meta:
        ordering = ['-level', 'name']
        verbose_name = '参赛选手'
        verbose_name_plural = '参赛选手'


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams', verbose_name='赛事')
    team_name = models.CharField('队伍名称', max_length=100)
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='as_player1', verbose_name='选手1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='as_player2', verbose_name='选手2')

    def __str__(self):
        return self.team_name

    class Meta:
        unique_together = ('event', 'team_name')
        verbose_name = '双打队伍'
        verbose_name_plural = '双打队伍'


class Match(models.Model):
    ROUND_CHOICES = [
        ('normal', '常规赛'),
        ('quarter', '1/4决赛'),
        ('semi', '半决赛'),
        ('final', '决赛'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='matches', verbose_name='赛事')
    round = models.CharField('轮次', max_length=20, choices=ROUND_CHOICES)
    match_number = models.PositiveIntegerField('场次编号')
    team1 = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='as_team1', verbose_name='队伍1')
    team2 = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='as_team2', verbose_name='队伍2')
    winner = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_matches', verbose_name='胜方')
    score = models.CharField('比分', max_length=50, blank=True)

    def __str__(self):
        return f"{self.get_round_display()} - 第{self.match_number}场"

    class Meta:
        unique_together = ('event', 'round', 'match_number')
        verbose_name = '对阵比赛'
        verbose_name_plural = '对阵比赛'