from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.helpers import cross_downstream
from datetime import datetime, timedelta


default_args = {
    'owner': 'flosports',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'email': ['andrew.therin@flosports.tv'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'cthulhu_v2',
    max_active_runs=1,
    catchup=False,
    default_args=default_args,
    schedule_interval=timedelta(days=365)
)
fs_dw_schema_evt_site = BashOperator(
    task_id='fs_dw_schema_evt_site',
    bash_command='echo "fs_dw_schema.evt_site"',
    dag=dag
)

fs_dw_schema_evt_right = BashOperator(
    task_id='fs_dw_schema_evt_right',
    bash_command='echo "fs_dw_schema.evt_right"',
    dag=dag
)

fs_util_stripe_charge_event = BashOperator(
    task_id='fs_util_stripe_charge_event',
    bash_command='echo "fs_util.stripe_charge_event"',
    dag=dag
)

fs_dw_schema_evt_ad_campaign = BashOperator(
    task_id='fs_dw_schema_evt_ad_campaign',
    bash_command='echo "fs_dw_schema.evt_ad_campaign"',
    dag=dag
)

fs_dw_schema_evt_user_zendesk = BashOperator(
    task_id='fs_dw_schema_evt_user_zendesk',
    bash_command='echo "fs_dw_schema.evt_user_zendesk"',
    dag=dag
)

fs_dw_schema_evt_user_ios = BashOperator(
    task_id='fs_dw_schema_evt_user_ios',
    bash_command='echo "fs_dw_schema.evt_user_ios"',
    dag=dag
)

fs_dw_schema_evt_user_android = BashOperator(
    task_id='fs_dw_schema_evt_user_android',
    bash_command='echo "fs_dw_schema.evt_user_android"',
    dag=dag
)

fs_dw_schema_evt_user_tv_apps = BashOperator(
    task_id='fs_dw_schema_evt_user_tv_apps',
    bash_command='echo "fs_dw_schema.evt_user_tv_apps"',
    dag=dag
)

fs_dw_schema_evt_ticket = BashOperator(
    task_id='fs_dw_schema_evt_ticket',
    bash_command='echo "fs_dw_schema.evt_ticket"',
    dag=dag
)

fs_dw_schema_evt_user_promoter = BashOperator(
    task_id='fs_dw_schema_evt_user_promoter',
    bash_command='echo "fs_dw_schema.evt_user_promoter"',
    dag=dag
)

fs_dw_schema_evt_promoter_campaign_metrics = BashOperator(
    task_id='fs_dw_schema_evt_promoter_campaign_metrics',
    bash_command='echo "fs_dw_schema.evt_promoter_campaign_metrics"',
    dag=dag
)

fs_dw_schema_evt_ad = BashOperator(
    task_id='fs_dw_schema_evt_ad',
    bash_command='echo "fs_dw_schema.evt_ad"',
    dag=dag
)

fs_util_bot_map = BashOperator(
    task_id='fs_util_bot_map',
    bash_command='echo "fs_util.bot_map"',
    dag=dag
)

fs_reports_rights_agg = BashOperator(
    task_id='fs_reports_rights_agg',
    bash_command='echo "fs_reports.rights_agg"',
    dag=dag
)

fs_util_stripe_balance_transaction_fee_details = BashOperator(
    task_id='fs_util_stripe_balance_transaction_fee_details',
    bash_command='echo "fs_util.stripe_balance_transaction_fee_details"',
    dag=dag
)

fs_util_evt_date = BashOperator(
    task_id='fs_util_evt_date',
    bash_command='echo "fs_util.evt_date"',
    dag=dag
)

fs_dw_schema_evt_opp_rights = BashOperator(
    task_id='fs_dw_schema_evt_opp_rights',
    bash_command='echo "fs_dw_schema.evt_opp_rights"',
    dag=dag
)

fs_dw_schema_evt_rights_cost = BashOperator(
    task_id='fs_dw_schema_evt_rights_cost',
    bash_command='echo "fs_dw_schema.evt_rights_cost"',
    dag=dag
)

fs_dw_schema_evt_budget_approval = BashOperator(
    task_id='fs_dw_schema_evt_budget_approval',
    bash_command='echo "fs_dw_schema.evt_budget_approval"',
    dag=dag
)

fs_dw_schema_evt_kim_activity_assignment = BashOperator(
    task_id='fs_dw_schema_evt_kim_activity_assignment',
    bash_command='echo "fs_dw_schema.evt_kim_activity_assignment"',
    dag=dag
)

fs_dw_schema_evt_kim_resource = BashOperator(
    task_id='fs_dw_schema_evt_kim_resource',
    bash_command='echo "fs_dw_schema.evt_kim_resource"',
    dag=dag
)

fs_dw_schema_evt_opp_events = BashOperator(
    task_id='fs_dw_schema_evt_opp_events',
    bash_command='echo "fs_dw_schema.evt_opp_events"',
    dag=dag
)

fs_dw_schema_evt_kim_proposal = BashOperator(
    task_id='fs_dw_schema_evt_kim_proposal',
    bash_command='echo "fs_dw_schema.evt_kim_proposal"',
    dag=dag
)

fs_dw_schema_evt_kim_delivery_group = BashOperator(
    task_id='fs_dw_schema_evt_kim_delivery_group',
    bash_command='echo "fs_dw_schema.evt_kim_delivery_group"',
    dag=dag
)

fs_dw_schema_evt_general_events = BashOperator(
    task_id='fs_dw_schema_evt_general_events',
    bash_command='echo "fs_dw_schema.evt_general_events"',
    dag=dag
)

fs_dw_schema_evt_kim_activity_role = BashOperator(
    task_id='fs_dw_schema_evt_kim_activity_role',
    bash_command='echo "fs_dw_schema.evt_kim_activity_role"',
    dag=dag
)

fs_reports_oracle_surveys = BashOperator(
    task_id='fs_reports_oracle_surveys',
    bash_command='echo "fs_reports.oracle_surveys"',
    dag=dag
)

fs_dw_schema_evt_user_youbora = BashOperator(
    task_id='fs_dw_schema_evt_user_youbora',
    bash_command='echo "fs_dw_schema.evt_user_youbora"',
    dag=dag
)

fs_util_stripe_invoices = BashOperator(
    task_id='fs_util_stripe_invoices',
    bash_command='echo "fs_util.stripe_invoices"',
    dag=dag
)

fs_dw_schema_evt_invoice = BashOperator(
    task_id='fs_dw_schema_evt_invoice',
    bash_command='echo "fs_dw_schema.evt_invoice"',
    dag=dag
)

fs_dw_schema_evt_card = BashOperator(
    task_id='fs_dw_schema_evt_card',
    bash_command='echo "fs_dw_schema.evt_card"',
    dag=dag
)

fs_dw_schema_evt_dispute = BashOperator(
    task_id='fs_dw_schema_evt_dispute',
    bash_command='echo "fs_dw_schema.evt_dispute"',
    dag=dag
)

fs_dw_schema_evt_promoter_campaign = BashOperator(
    task_id='fs_dw_schema_evt_promoter_campaign',
    bash_command='echo "fs_dw_schema.evt_promoter_campaign"',
    dag=dag
)

fs_dw_schema_evt_user_flocore = BashOperator(
    task_id='fs_dw_schema_evt_user_flocore',
    bash_command='echo "fs_dw_schema.evt_user_flocore"',
    dag=dag
)

fs_dw_schema_evt_user_stripe = BashOperator(
    task_id='fs_dw_schema_evt_user_stripe',
    bash_command='echo "fs_dw_schema.evt_user_stripe"',
    dag=dag
)

fs_dw_schema_evt_user_web = BashOperator(
    task_id='fs_dw_schema_evt_user_web',
    bash_command='echo "fs_dw_schema.evt_user_web"',
    dag=dag
)

fs_util_itunes_site_map = BashOperator(
    task_id='fs_util_itunes_site_map',
    bash_command='echo "fs_util.itunes_site_map"',
    dag=dag
)

fs_util_rtid_map = BashOperator(
    task_id='fs_util_rtid_map',
    bash_command='echo "fs_util.rtid_map"',
    dag=dag
)

fs_dw_schema_fact_ad_campaign = BashOperator(
    task_id='fs_dw_schema_fact_ad_campaign',
    bash_command='echo "fs_dw_schema.fact_ad_campaign"',
    dag=dag
)

fs_dw_schema_evt_plan_stripe = BashOperator(
    task_id='fs_dw_schema_evt_plan_stripe',
    bash_command='echo "fs_dw_schema.evt_plan_stripe"',
    dag=dag
)

fs_dw_schema_fact_ad = BashOperator(
    task_id='fs_dw_schema_fact_ad',
    bash_command='echo "fs_dw_schema.fact_ad"',
    dag=dag
)

fs_dw_schema_evt_content_flocore = BashOperator(
    task_id='fs_dw_schema_evt_content_flocore',
    bash_command='echo "fs_dw_schema.evt_content_flocore"',
    dag=dag
)

cross_downstream([fs_dw_schema_evt_site, fs_dw_schema_evt_right, fs_util_stripe_charge_event, fs_dw_schema_evt_ad_campaign, fs_dw_schema_evt_user_zendesk, fs_dw_schema_evt_user_ios, fs_dw_schema_evt_user_android, fs_dw_schema_evt_user_tv_apps, fs_dw_schema_evt_ticket, fs_dw_schema_evt_user_promoter, fs_dw_schema_evt_promoter_campaign_metrics, fs_dw_schema_evt_ad, fs_util_bot_map, fs_reports_rights_agg, fs_util_stripe_balance_transaction_fee_details, fs_util_evt_date, fs_dw_schema_evt_opp_rights, fs_dw_schema_evt_rights_cost, fs_dw_schema_evt_budget_approval, fs_dw_schema_evt_kim_activity_assignment, fs_dw_schema_evt_kim_resource, fs_dw_schema_evt_opp_events, fs_dw_schema_evt_kim_proposal, fs_dw_schema_evt_kim_delivery_group, fs_dw_schema_evt_general_events, fs_dw_schema_evt_kim_activity_role, fs_reports_oracle_surveys, fs_dw_schema_evt_user_youbora, fs_util_stripe_invoices], [fs_dw_schema_evt_invoice, fs_dw_schema_evt_card, fs_dw_schema_evt_dispute, fs_dw_schema_evt_promoter_campaign, fs_dw_schema_evt_user_flocore, fs_dw_schema_evt_user_stripe, fs_dw_schema_evt_user_web, fs_util_itunes_site_map, fs_util_rtid_map, fs_dw_schema_fact_ad_campaign, fs_dw_schema_evt_plan_stripe, fs_dw_schema_fact_ad, fs_dw_schema_evt_content_flocore])
fs_dw_schema_evt_content = BashOperator(
    task_id='fs_dw_schema_evt_content',
    bash_command='echo "fs_dw_schema.evt_content"',
    dag=dag
)

fs_dw_schema_evt_user_email = BashOperator(
    task_id='fs_dw_schema_evt_user_email',
    bash_command='echo "fs_dw_schema.evt_user_email"',
    dag=dag
)

fs_dw_schema_evt_user_itunes = BashOperator(
    task_id='fs_dw_schema_evt_user_itunes',
    bash_command='echo "fs_dw_schema.evt_user_itunes"',
    dag=dag
)

fs_dw_schema_fact_promoter_campaign = BashOperator(
    task_id='fs_dw_schema_fact_promoter_campaign',
    bash_command='echo "fs_dw_schema.fact_promoter_campaign"',
    dag=dag
)

cross_downstream([fs_dw_schema_evt_invoice, fs_dw_schema_evt_card, fs_dw_schema_evt_dispute, fs_dw_schema_evt_promoter_campaign, fs_dw_schema_evt_user_flocore, fs_dw_schema_evt_user_stripe, fs_dw_schema_evt_user_web, fs_util_itunes_site_map, fs_util_rtid_map, fs_dw_schema_fact_ad_campaign, fs_dw_schema_evt_plan_stripe, fs_dw_schema_fact_ad, fs_dw_schema_evt_content_flocore], [fs_dw_schema_evt_content, fs_dw_schema_evt_user_email, fs_dw_schema_evt_user_itunes, fs_dw_schema_fact_promoter_campaign])
fs_util_user_map = BashOperator(
    task_id='fs_util_user_map',
    bash_command='echo "fs_util.user_map"',
    dag=dag
)

fs_dw_schema_evt_coverage = BashOperator(
    task_id='fs_dw_schema_evt_coverage',
    bash_command='echo "fs_dw_schema.evt_coverage"',
    dag=dag
)

cross_downstream([fs_dw_schema_evt_content, fs_dw_schema_evt_user_email, fs_dw_schema_evt_user_itunes, fs_dw_schema_fact_promoter_campaign], [fs_util_user_map, fs_dw_schema_evt_coverage])
fs_dw_schema_fact_itunes = BashOperator(
    task_id='fs_dw_schema_fact_itunes',
    bash_command='echo "fs_dw_schema.fact_itunes"',
    dag=dag
)

fs_dw_schema_evt_charge_stripe = BashOperator(
    task_id='fs_dw_schema_evt_charge_stripe',
    bash_command='echo "fs_dw_schema.evt_charge_stripe"',
    dag=dag
)

fs_dw_schema_fact_right = BashOperator(
    task_id='fs_dw_schema_fact_right',
    bash_command='echo "fs_dw_schema.fact_right"',
    dag=dag
)

fs_dw_schema_evt_user = BashOperator(
    task_id='fs_dw_schema_evt_user',
    bash_command='echo "fs_dw_schema.evt_user"',
    dag=dag
)

fs_dw_schema_fact_visits_ios = BashOperator(
    task_id='fs_dw_schema_fact_visits_ios',
    bash_command='echo "fs_dw_schema.fact_visits_ios"',
    dag=dag
)

fs_dw_schema_fact_visits_tv_apps = BashOperator(
    task_id='fs_dw_schema_fact_visits_tv_apps',
    bash_command='echo "fs_dw_schema.fact_visits_tv_apps"',
    dag=dag
)

fs_dw_schema_fact_visits_android = BashOperator(
    task_id='fs_dw_schema_fact_visits_android',
    bash_command='echo "fs_dw_schema.fact_visits_android"',
    dag=dag
)

fs_dw_schema_fact_funnel_ios = BashOperator(
    task_id='fs_dw_schema_fact_funnel_ios',
    bash_command='echo "fs_dw_schema.fact_funnel_ios"',
    dag=dag
)

fs_dw_schema_fact_content_android = BashOperator(
    task_id='fs_dw_schema_fact_content_android',
    bash_command='echo "fs_dw_schema.fact_content_android"',
    dag=dag
)

fs_dw_schema_fact_youbora_web = BashOperator(
    task_id='fs_dw_schema_fact_youbora_web',
    bash_command='echo "fs_dw_schema.fact_youbora_web"',
    dag=dag
)

fs_dw_schema_evt_promoter_feedback = BashOperator(
    task_id='fs_dw_schema_evt_promoter_feedback',
    bash_command='echo "fs_dw_schema.evt_promoter_feedback"',
    dag=dag
)

fs_dw_schema_fact_content_tv_apps = BashOperator(
    task_id='fs_dw_schema_fact_content_tv_apps',
    bash_command='echo "fs_dw_schema.fact_content_tv_apps"',
    dag=dag
)

fs_dw_schema_fact_content_ios = BashOperator(
    task_id='fs_dw_schema_fact_content_ios',
    bash_command='echo "fs_dw_schema.fact_content_ios"',
    dag=dag
)

fs_dw_schema_fact_ticket = BashOperator(
    task_id='fs_dw_schema_fact_ticket',
    bash_command='echo "fs_dw_schema.fact_ticket"',
    dag=dag
)

fs_dw_schema_fact_load_time_web = BashOperator(
    task_id='fs_dw_schema_fact_load_time_web',
    bash_command='echo "fs_dw_schema.fact_load_time_web"',
    dag=dag
)

fs_dw_schema_fact_experiment_viewed = BashOperator(
    task_id='fs_dw_schema_fact_experiment_viewed',
    bash_command='echo "fs_dw_schema.fact_experiment_viewed"',
    dag=dag
)

cross_downstream([fs_util_user_map, fs_dw_schema_evt_coverage], [fs_dw_schema_fact_itunes, fs_dw_schema_evt_charge_stripe, fs_dw_schema_fact_right, fs_dw_schema_evt_user, fs_dw_schema_fact_visits_ios, fs_dw_schema_fact_visits_tv_apps, fs_dw_schema_fact_visits_android, fs_dw_schema_fact_funnel_ios, fs_dw_schema_fact_content_android, fs_dw_schema_fact_youbora_web, fs_dw_schema_evt_promoter_feedback, fs_dw_schema_fact_content_tv_apps, fs_dw_schema_fact_content_ios, fs_dw_schema_fact_ticket, fs_dw_schema_fact_load_time_web, fs_dw_schema_fact_experiment_viewed])
fs_dw_schema_fact_youbora = BashOperator(
    task_id='fs_dw_schema_fact_youbora',
    bash_command='echo "fs_dw_schema.fact_youbora"',
    dag=dag
)

fs_dw_schema_evt_plan_itunes = BashOperator(
    task_id='fs_dw_schema_evt_plan_itunes',
    bash_command='echo "fs_dw_schema.evt_plan_itunes"',
    dag=dag
)

fs_dw_schema_evt_subscription_itunes = BashOperator(
    task_id='fs_dw_schema_evt_subscription_itunes',
    bash_command='echo "fs_dw_schema.evt_subscription_itunes"',
    dag=dag
)

fs_dw_schema_evt_charge_itunes = BashOperator(
    task_id='fs_dw_schema_evt_charge_itunes',
    bash_command='echo "fs_dw_schema.evt_charge_itunes"',
    dag=dag
)

fs_dw_schema_evt_subscription_stripe = BashOperator(
    task_id='fs_dw_schema_evt_subscription_stripe',
    bash_command='echo "fs_dw_schema.evt_subscription_stripe"',
    dag=dag
)

fs_dw_schema_fact_promoter_feedback = BashOperator(
    task_id='fs_dw_schema_fact_promoter_feedback',
    bash_command='echo "fs_dw_schema.fact_promoter_feedback"',
    dag=dag
)

fs_reports_ad_agg = BashOperator(
    task_id='fs_reports_ad_agg',
    bash_command='echo "fs_reports.ad_agg"',
    dag=dag
)

cross_downstream([fs_dw_schema_fact_itunes, fs_dw_schema_evt_charge_stripe, fs_dw_schema_fact_right, fs_dw_schema_evt_user, fs_dw_schema_fact_visits_ios, fs_dw_schema_fact_visits_tv_apps, fs_dw_schema_fact_visits_android, fs_dw_schema_fact_funnel_ios, fs_dw_schema_fact_content_android, fs_dw_schema_fact_youbora_web, fs_dw_schema_evt_promoter_feedback, fs_dw_schema_fact_content_tv_apps, fs_dw_schema_fact_content_ios, fs_dw_schema_fact_ticket, fs_dw_schema_fact_load_time_web, fs_dw_schema_fact_experiment_viewed], [fs_dw_schema_fact_youbora, fs_dw_schema_evt_plan_itunes, fs_dw_schema_evt_subscription_itunes, fs_dw_schema_evt_charge_itunes, fs_dw_schema_evt_subscription_stripe, fs_dw_schema_fact_promoter_feedback, fs_reports_ad_agg])
fs_dw_schema_evt_plan = BashOperator(
    task_id='fs_dw_schema_evt_plan',
    bash_command='echo "fs_dw_schema.evt_plan"',
    dag=dag
)

fs_dw_schema_evt_subscription = BashOperator(
    task_id='fs_dw_schema_evt_subscription',
    bash_command='echo "fs_dw_schema.evt_subscription"',
    dag=dag
)

fs_dw_schema_evt_charge = BashOperator(
    task_id='fs_dw_schema_evt_charge',
    bash_command='echo "fs_dw_schema.evt_charge"',
    dag=dag
)

fs_dw_schema_fact_live_activity = BashOperator(
    task_id='fs_dw_schema_fact_live_activity',
    bash_command='echo "fs_dw_schema.fact_live_activity"',
    dag=dag
)

fs_dw_schema_fact_charge_itunes = BashOperator(
    task_id='fs_dw_schema_fact_charge_itunes',
    bash_command='echo "fs_dw_schema.fact_charge_itunes"',
    dag=dag
)

fs_dw_schema_fact_video_youbora = BashOperator(
    task_id='fs_dw_schema_fact_video_youbora',
    bash_command='echo "fs_dw_schema.fact_video_youbora"',
    dag=dag
)

fs_dw_schema_fact_video_activity = BashOperator(
    task_id='fs_dw_schema_fact_video_activity',
    bash_command='echo "fs_dw_schema.fact_video_activity"',
    dag=dag
)

fs_dw_schema_fact_incidents = BashOperator(
    task_id='fs_dw_schema_fact_incidents',
    bash_command='echo "fs_dw_schema.fact_incidents"',
    dag=dag
)

cross_downstream([fs_dw_schema_fact_youbora, fs_dw_schema_evt_plan_itunes, fs_dw_schema_evt_subscription_itunes, fs_dw_schema_evt_charge_itunes, fs_dw_schema_evt_subscription_stripe, fs_dw_schema_fact_promoter_feedback, fs_reports_ad_agg], [fs_dw_schema_evt_plan, fs_dw_schema_evt_subscription, fs_dw_schema_evt_charge, fs_dw_schema_fact_live_activity, fs_dw_schema_fact_charge_itunes, fs_dw_schema_fact_video_youbora, fs_dw_schema_fact_video_activity, fs_dw_schema_fact_incidents])
fs_dw_schema_fact_activity_web = BashOperator(
    task_id='fs_dw_schema_fact_activity_web',
    bash_command='echo "fs_dw_schema.fact_activity_web"',
    dag=dag
)

fs_dw_schema_fact_dispute = BashOperator(
    task_id='fs_dw_schema_fact_dispute',
    bash_command='echo "fs_dw_schema.fact_dispute"',
    dag=dag
)

fs_dw_schema_fact_charge_stripe = BashOperator(
    task_id='fs_dw_schema_fact_charge_stripe',
    bash_command='echo "fs_dw_schema.fact_charge_stripe"',
    dag=dag
)

fs_dw_schema_fact_video = BashOperator(
    task_id='fs_dw_schema_fact_video',
    bash_command='echo "fs_dw_schema.fact_video"',
    dag=dag
)

fs_dw_schema_fact_live_concurrents = BashOperator(
    task_id='fs_dw_schema_fact_live_concurrents',
    bash_command='echo "fs_dw_schema.fact_live_concurrents"',
    dag=dag
)

fs_reports_mrr_agg = BashOperator(
    task_id='fs_reports_mrr_agg',
    bash_command='echo "fs_reports.mrr_agg"',
    dag=dag
)

fs_dw_schema_fact_charge_failed = BashOperator(
    task_id='fs_dw_schema_fact_charge_failed',
    bash_command='echo "fs_dw_schema.fact_charge_failed"',
    dag=dag
)

cross_downstream([fs_dw_schema_evt_plan, fs_dw_schema_evt_subscription, fs_dw_schema_evt_charge, fs_dw_schema_fact_live_activity, fs_dw_schema_fact_charge_itunes, fs_dw_schema_fact_video_youbora, fs_dw_schema_fact_video_activity, fs_dw_schema_fact_incidents], [fs_dw_schema_fact_activity_web, fs_dw_schema_fact_dispute, fs_dw_schema_fact_charge_stripe, fs_dw_schema_fact_video, fs_dw_schema_fact_live_concurrents, fs_reports_mrr_agg, fs_dw_schema_fact_charge_failed])
fs_dw_schema_fact_charge = BashOperator(
    task_id='fs_dw_schema_fact_charge',
    bash_command='echo "fs_dw_schema.fact_charge"',
    dag=dag
)

fs_dw_schema_fact_funnel_web = BashOperator(
    task_id='fs_dw_schema_fact_funnel_web',
    bash_command='echo "fs_dw_schema.fact_funnel_web"',
    dag=dag
)

fs_dw_schema_fact_visits_web = BashOperator(
    task_id='fs_dw_schema_fact_visits_web',
    bash_command='echo "fs_dw_schema.fact_visits_web"',
    dag=dag
)

fs_dw_schema_fact_content_web = BashOperator(
    task_id='fs_dw_schema_fact_content_web',
    bash_command='echo "fs_dw_schema.fact_content_web"',
    dag=dag
)

fs_dw_schema_fact_activity = BashOperator(
    task_id='fs_dw_schema_fact_activity',
    bash_command='echo "fs_dw_schema.fact_activity"',
    dag=dag
)

cross_downstream([fs_dw_schema_fact_activity_web, fs_dw_schema_fact_dispute, fs_dw_schema_fact_charge_stripe, fs_dw_schema_fact_video, fs_dw_schema_fact_live_concurrents, fs_reports_mrr_agg, fs_dw_schema_fact_charge_failed], [fs_dw_schema_fact_charge, fs_dw_schema_fact_funnel_web, fs_dw_schema_fact_visits_web, fs_dw_schema_fact_content_web, fs_dw_schema_fact_activity])
fs_dw_schema_fact_visits = BashOperator(
    task_id='fs_dw_schema_fact_visits',
    bash_command='echo "fs_dw_schema.fact_visits"',
    dag=dag
)

fs_dw_schema_fact_content = BashOperator(
    task_id='fs_dw_schema_fact_content',
    bash_command='echo "fs_dw_schema.fact_content"',
    dag=dag
)

fs_util_charge_interval_map = BashOperator(
    task_id='fs_util_charge_interval_map',
    bash_command='echo "fs_util.charge_interval_map"',
    dag=dag
)

fs_dw_schema_fact_funnel = BashOperator(
    task_id='fs_dw_schema_fact_funnel',
    bash_command='echo "fs_dw_schema.fact_funnel"',
    dag=dag
)

fs_reports_sub_agg = BashOperator(
    task_id='fs_reports_sub_agg',
    bash_command='echo "fs_reports.sub_agg"',
    dag=dag
)

cross_downstream([fs_dw_schema_fact_charge, fs_dw_schema_fact_funnel_web, fs_dw_schema_fact_visits_web, fs_dw_schema_fact_content_web, fs_dw_schema_fact_activity], [fs_dw_schema_fact_visits, fs_dw_schema_fact_content, fs_util_charge_interval_map, fs_dw_schema_fact_funnel, fs_reports_sub_agg])
fs_reports_charge_agg = BashOperator(
    task_id='fs_reports_charge_agg',
    bash_command='echo "fs_reports.charge_agg"',
    dag=dag
)

fs_reports_viewership = BashOperator(
    task_id='fs_reports_viewership',
    bash_command='echo "fs_reports.viewership"',
    dag=dag
)

cross_downstream([fs_dw_schema_fact_visits, fs_dw_schema_fact_content, fs_util_charge_interval_map, fs_dw_schema_fact_funnel, fs_reports_sub_agg], [fs_reports_charge_agg, fs_reports_viewership])
fs_reports_attribution_agg = BashOperator(
    task_id='fs_reports_attribution_agg',
    bash_command='echo "fs_reports.attribution_agg"',
    dag=dag
)

cross_downstream([fs_reports_charge_agg, fs_reports_viewership], [fs_reports_attribution_agg])
fs_reports_ref_attribution_agg = BashOperator(
    task_id='fs_reports_ref_attribution_agg',
    bash_command='echo "fs_reports.ref_attribution_agg"',
    dag=dag
)

fs_reports_event_agg = BashOperator(
    task_id='fs_reports_event_agg',
    bash_command='echo "fs_reports.event_agg"',
    dag=dag
)

cross_downstream([fs_reports_attribution_agg], [fs_reports_ref_attribution_agg, fs_reports_event_agg])
