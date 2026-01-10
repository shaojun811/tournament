from django.contrib import admin
from .models import Event, Player, Team, Match, EventType

# 美化后台整体标题
admin.site.site_header = 'Pickleball 赛事管理后台'
admin.site.site_title = '赛事管理'
admin.site.index_title = '欢迎来到 Pickleball 双打赛事管理系统'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'start_time', 'location', 'status']
    list_filter = ['status', 'event_type', 'start_time']
    search_fields = ['name', 'location']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'event_type', 'start_time', 'end_time', 'location', 'status')
        }),
        ('详细描述', {
            'fields': ('description',),
            'classes': ('collapse',),  # 可折叠
        }),
    )

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'level', 'created_at']
    list_filter = ['gender', 'level', 'created_at']
    search_fields = ['name']
    fieldsets = (
        ('选手信息', {
            'fields': ('name', 'gender', 'level')
        }),
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'event', 'get_player1', 'get_player2']
    list_filter = ['event']
    search_fields = ['team_name']

    def get_player1(self, obj):
        return f"{obj.player1.name} ({obj.player1.level})"
    get_player1.short_description = '选手1'

    def get_player2(self, obj):
        return f"{obj.player2.name} ({obj.player2.level})"
    get_player2.short_description = '选手2'

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['event', 'get_round_display', 'match_number', 'team1', 'team2', 'winner', 'score']
    list_filter = ['event', 'round']
    fieldsets = (
        ('对阵信息', {
            'fields': ('event', 'round', 'match_number', 'team1', 'team2')
        }),
        ('比赛结果', {
            'fields': ('winner', 'score'),
            'classes': ('collapse',),
        }),
    )


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']