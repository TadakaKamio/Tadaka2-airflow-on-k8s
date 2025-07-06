<!DOCTYPE html>
<html lang="ja-JP" class="theme-auto">
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>esg05/register_public_factor.py at 81d9328a5f2a8b9bd976f47f3bd5163081c37afb - esg05 - TDH Temporary Gitea</title>
	<link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiVERIIFRlbXBvcmFyeSBHaXRlYSIsInNob3J0X25hbWUiOiJUREggVGVtcG9yYXJ5IEdpdGVhIiwic3RhcnRfdXJsIjoiaHR0cDovL2dpdC5leGFtcGxlLmNvbS8iLCJpY29ucyI6W3sic3JjIjoiaHR0cDovL2dpdC5leGFtcGxlLmNvbS9hc3NldHMvaW1nL2xvZ28ucG5nIiwidHlwZSI6ImltYWdlL3BuZyIsInNpemVzIjoiNTEyeDUxMiJ9LHsic3JjIjoiaHR0cDovL2dpdC5leGFtcGxlLmNvbS9hc3NldHMvaW1nL2xvZ28uc3ZnIiwidHlwZSI6ImltYWdlL3N2Zyt4bWwiLCJzaXplcyI6IjUxMng1MTIifV19">
	<meta name="author" content="hd-dev-user01">
	<meta name="description" content="esg05">
	<meta name="keywords" content="go,git,self-hosted,gitea">
	<meta name="referrer" content="no-referrer">


	<link rel="alternate" type="application/atom+xml" title="" href="/hd-dev-user01/esg05.atom">
	<link rel="alternate" type="application/rss+xml" title="" href="/hd-dev-user01/esg05.rss">

	<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
	<link rel="alternate icon" href="/assets/img/favicon.png" type="image/png">
	
<script>
	
	window.addEventListener('error', function(e) {window._globalHandlerErrors=window._globalHandlerErrors||[]; window._globalHandlerErrors.push(e);});
	window.addEventListener('unhandledrejection', function(e) {window._globalHandlerErrors=window._globalHandlerErrors||[]; window._globalHandlerErrors.push(e);});
	window.config = {
		appUrl: 'http:\/\/git.example.com\/',
		appSubUrl: '',
		assetVersionEncoded: encodeURIComponent('1.21.5'), 
		assetUrlPrefix: '\/assets',
		runModeIsProd:  true ,
		customEmojis: {"codeberg":":codeberg:","git":":git:","gitea":":gitea:","github":":github:","gitlab":":gitlab:","gogs":":gogs:"},
		csrfToken: '2z24Lq7Pf1CO6d8N4oP2T25w50Y6MTc1MTYyMjM2MTcxMzQ0NzkwOQ',
		pageData: {},
		notificationSettings: {"EventSourceUpdateTime":10000,"MaxTimeout":60000,"MinTimeout":10000,"TimeoutStep":10000}, 
		enableTimeTracking:  true ,
		
		mermaidMaxSourceCharacters:  5000 ,
		
		i18n: {
			copy_success: "コピーされました！",
			copy_error: "コピーに失敗しました",
			error_occurred: "エラーが発生しました．",
			network_error: "ネットワークエラー",
			remove_label_str: "アイテム「%s」を削除",
			modal_confirm: "了解",
			modal_cancel: "キャンセル",
		},
	};
	
	window.config.pageData = window.config.pageData || {};
</script>
<script src="/assets/js/webcomponents.js?v=1.21.5"></script>

	<noscript>
		<style>
			.dropdown:hover > .menu { display: block; }
			.ui.secondary.menu .dropdown.item > .menu { margin-top: 0; }
		</style>
	</noscript>
	
	
		<meta property="og:title" content="esg05/register_public_factor.py at 81d9328a5f2a8b9bd976f47f3bd5163081c37afb">
		<meta property="og:url" content="http://git.example.com//hd-dev-user01/esg05/src/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py">
		
	
	<meta property="og:type" content="object">
	
		<meta property="og:image" content="https://secure.gravatar.com/avatar/db81f31b7ab4cc356623b763d1b08680?d=identicon">
	

<meta property="og:site_name" content="TDH Temporary Gitea">

	<link rel="stylesheet" href="/assets/css/index.css?v=1.21.5">

	
		<link rel="stylesheet" href="/assets/css/theme-auto.css?v=1.21.5">
	


	
</head>
<body>
	
	

	<div class="full height">
		<noscript>このウェブサイトにはJavaScriptが必要です。</noscript>

		

		
			

	


<nav id="navbar" aria-label="ナビゲーションバー">
	<div class="navbar-left ui secondary menu">
		
		<a class="item" id="navbar-logo" href="/" aria-label="ダッシュボード">
			<img width="30" height="30" src="/assets/img/logo.svg" alt="ロゴ" aria-hidden="true">
		</a>

		
		<div class="ui secondary menu item navbar-mobile-right">
			
			<a id="mobile-notifications-icon" class="item gt-w-auto gt-p-3" href="/notifications" data-tooltip-content="通知" aria-label="通知">
				<div class="gt-relative">
					<svg viewBox="0 0 16 16" class="svg octicon-bell" aria-hidden="true" width="16" height="16"><path d="M8 16a2 2 0 0 0 1.985-1.75c.017-.137-.097-.25-.235-.25h-3.5c-.138 0-.252.113-.235.25A2 2 0 0 0 8 16ZM3 5a5 5 0 0 1 10 0v2.947c0 .05.015.098.042.139l1.703 2.555A1.519 1.519 0 0 1 13.482 13H2.518a1.516 1.516 0 0 1-1.263-2.36l1.703-2.554A.255.255 0 0 0 3 7.947Zm5-3.5A3.5 3.5 0 0 0 4.5 5v2.947c0 .346-.102.683-.294.97l-1.703 2.556a.017.017 0 0 0-.003.01l.001.006c0 .002.002.004.004.006l.006.004.007.001h10.964l.007-.001.006-.004.004-.006.001-.007a.017.017 0 0 0-.003-.01l-1.703-2.554a1.745 1.745 0 0 1-.294-.97V5A3.5 3.5 0 0 0 8 1.5Z"/></svg>
					<span class="notification_count">30</span>
				</div>
			</a>
			
			<button class="item gt-w-auto ui icon mini button gt-p-3 gt-m-0" id="navbar-expand-toggle"><svg viewBox="0 0 16 16" class="svg octicon-three-bars" aria-hidden="true" width="16" height="16"><path d="M1 2.75A.75.75 0 0 1 1.75 2h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 2.75Zm0 5A.75.75 0 0 1 1.75 7h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 7.75ZM1.75 12h12.5a.75.75 0 0 1 0 1.5H1.75a.75.75 0 0 1 0-1.5Z"/></svg></button>
		</div>

		
		
			
				<a class="item" href="/issues">イシュー</a>
			
			
				<a class="item" href="/pulls">プルリクエスト</a>
			
			
				
					<a class="item" href="/milestones">マイルストーン</a>
				
			
			<a class="item" href="/explore/repos">エクスプローラー</a>
		

		

		
	</div>

	
	<div class="navbar-right ui secondary menu">
		
			
			<a class="active-stopwatch-trigger item gt-mx-0 gt-hidden" href="" title="進行中のタイムトラッカー">
				<div class="gt-relative">
					<svg viewBox="0 0 16 16" class="svg octicon-stopwatch" aria-hidden="true" width="16" height="16"><path d="M5.75.75A.75.75 0 0 1 6.5 0h3a.75.75 0 0 1 0 1.5h-.75v1l-.001.041a6.724 6.724 0 0 1 3.464 1.435l.007-.006.75-.75a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734l-.75.75-.006.007a6.75 6.75 0 1 1-10.548 0L2.72 5.03l-.75-.75a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018l.75.75.007.006A6.72 6.72 0 0 1 7.25 2.541V1.5H6.5a.75.75 0 0 1-.75-.75ZM8 14.5a5.25 5.25 0 1 0-.001-10.501A5.25 5.25 0 0 0 8 14.5Zm.389-6.7 1.33-1.33a.75.75 0 1 1 1.061 1.06L9.45 8.861A1.503 1.503 0 0 1 8 10.75a1.499 1.499 0 1 1 .389-2.95Z"/></svg>
					<span class="header-stopwatch-dot"></span>
				</div>
				<span class="mobile-only gt-ml-3">進行中のタイムトラッカー</span>
			</a>
			<div class="active-stopwatch-popup item tippy-target gt-p-3">
				<div class="gt-df gt-ac">
					<a class="stopwatch-link gt-df gt-ac" href="">
						<svg viewBox="0 0 16 16" class="gt-mr-3 svg octicon-issue-opened" aria-hidden="true" width="16" height="16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg>
						<span class="stopwatch-issue">#</span>
						<span class="ui primary label stopwatch-time gt-my-0 gt-mx-4" data-seconds="">
							
						</span>
					</a>
					<form class="stopwatch-commit" method="post" action="/times/stopwatch/toggle">
						<input type="hidden" name="_csrf" value="2z24Lq7Pf1CO6d8N4oP2T25w50Y6MTc1MTYyMjM2MTcxMzQ0NzkwOQ">
						<button
							type="submit"
							class="ui button mini compact basic icon"
							data-tooltip-content="タイマー 終了"
						><svg viewBox="0 0 16 16" class="svg octicon-square-fill" aria-hidden="true" width="16" height="16"><path d="M5.75 4h4.5c.966 0 1.75.784 1.75 1.75v4.5A1.75 1.75 0 0 1 10.25 12h-4.5A1.75 1.75 0 0 1 4 10.25v-4.5C4 4.784 4.784 4 5.75 4Z"/></svg></button>
					</form>
					<form class="stopwatch-cancel" method="post" action="/times/stopwatch/cancel">
						<input type="hidden" name="_csrf" value="2z24Lq7Pf1CO6d8N4oP2T25w50Y6MTc1MTYyMjM2MTcxMzQ0NzkwOQ">
						<button
							type="submit"
							class="ui button mini compact basic icon"
							data-tooltip-content="中止"
						><svg viewBox="0 0 16 16" class="svg octicon-trash" aria-hidden="true" width="16" height="16"><path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"/></svg></button>
					</form>
				</div>
			</div>
			

			<a class="item not-mobile gt-mx-0" href="/notifications" data-tooltip-content="通知" aria-label="通知">
				<div class="gt-relative">
					<svg viewBox="0 0 16 16" class="svg octicon-bell" aria-hidden="true" width="16" height="16"><path d="M8 16a2 2 0 0 0 1.985-1.75c.017-.137-.097-.25-.235-.25h-3.5c-.138 0-.252.113-.235.25A2 2 0 0 0 8 16ZM3 5a5 5 0 0 1 10 0v2.947c0 .05.015.098.042.139l1.703 2.555A1.519 1.519 0 0 1 13.482 13H2.518a1.516 1.516 0 0 1-1.263-2.36l1.703-2.554A.255.255 0 0 0 3 7.947Zm5-3.5A3.5 3.5 0 0 0 4.5 5v2.947c0 .346-.102.683-.294.97l-1.703 2.556a.017.017 0 0 0-.003.01l.001.006c0 .002.002.004.004.006l.006.004.007.001h10.964l.007-.001.006-.004.004-.006.001-.007a.017.017 0 0 0-.003-.01l-1.703-2.554a1.745 1.745 0 0 1-.294-.97V5A3.5 3.5 0 0 0 8 1.5Z"/></svg>
					<span class="notification_count">30</span>
				</div>
			</a>

			<div class="ui dropdown jump item gt-mx-0 gt-pr-3" data-tooltip-content="作成…">
				<span class="text">
					<svg viewBox="0 0 16 16" class="svg octicon-plus" aria-hidden="true" width="16" height="16"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"/></svg>
					<span class="not-mobile"><svg viewBox="0 0 16 16" class="svg octicon-triangle-down" aria-hidden="true" width="16" height="16"><path d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427Z"/></svg></span>
					<span class="mobile-only">作成…</span>
				</span>
				<div class="menu">
					<a class="item" href="/repo/create">
						<svg viewBox="0 0 16 16" class="svg octicon-plus" aria-hidden="true" width="16" height="16"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"/></svg> 新しいリポジトリ
					</a>
					
						<a class="item" href="/repo/migrate">
							<svg viewBox="0 0 16 16" class="svg octicon-repo-push" aria-hidden="true" width="16" height="16"><path d="M1 2.5A2.5 2.5 0 0 1 3.5 0h8.75a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0V1.5h-8a1 1 0 0 0-1 1v6.708A2.493 2.493 0 0 1 3.5 9h3.25a.75.75 0 0 1 0 1.5H3.5a1 1 0 0 0 0 2h5.75a.75.75 0 0 1 0 1.5H3.5A2.5 2.5 0 0 1 1 11.5Zm13.23 7.79h-.001l-1.224-1.224v6.184a.75.75 0 0 1-1.5 0V9.066L10.28 10.29a.75.75 0 0 1-1.06-1.061l2.505-2.504a.75.75 0 0 1 1.06 0L15.29 9.23a.751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018Z"/></svg> 新しい移行
						</a>
					
					
					<a class="item" href="/org/create">
						<svg viewBox="0 0 16 16" class="svg octicon-organization" aria-hidden="true" width="16" height="16"><path d="M1.75 16A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0h8.5C11.216 0 12 .784 12 1.75v12.5c0 .085-.006.168-.018.25h2.268a.25.25 0 0 0 .25-.25V8.285a.25.25 0 0 0-.111-.208l-1.055-.703a.749.749 0 1 1 .832-1.248l1.055.703c.487.325.779.871.779 1.456v5.965A1.75 1.75 0 0 1 14.25 16h-3.5a.766.766 0 0 1-.197-.026c-.099.017-.2.026-.303.026h-3a.75.75 0 0 1-.75-.75V14h-1v1.25a.75.75 0 0 1-.75.75Zm-.25-1.75c0 .138.112.25.25.25H4v-1.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 .75.75v1.25h2.25a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25ZM3.75 6h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 3.75A.75.75 0 0 1 3.75 3h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 3.75Zm4 3A.75.75 0 0 1 7.75 6h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 7 6.75ZM7.75 3h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 9.75A.75.75 0 0 1 3.75 9h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 9.75ZM7.75 9h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"/></svg> 新しい組織
					</a>
					
				</div>
			</div>

			<div class="ui dropdown jump item gt-mx-0 gt-pr-3" data-tooltip-content="プロフィールと設定…">
				<span class="text gt-df gt-ac">
					<img class="ui avatar gt-vm gt-mr-2" src="https://secure.gravatar.com/avatar/db81f31b7ab4cc356623b763d1b08680?d=identicon&s=48" title="hd-dev-user01" width="24" height="24"/>
					<span class="mobile-only gt-ml-3">hd-dev-user01</span>
					<span class="not-mobile"><svg viewBox="0 0 16 16" class="svg octicon-triangle-down" aria-hidden="true" width="16" height="16"><path d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427Z"/></svg></span>
				</span>
				<div class="menu user-menu">
					<div class="ui header">
						サインイン済み <strong>hd-dev-user01</strong>
					</div>

					<div class="divider"></div>
					<a class="item" href="/hd-dev-user01">
						<svg viewBox="0 0 16 16" class="svg octicon-person" aria-hidden="true" width="16" height="16"><path d="M10.561 8.073a6.005 6.005 0 0 1 3.432 5.142.75.75 0 1 1-1.498.07 4.5 4.5 0 0 0-8.99 0 .75.75 0 0 1-1.498-.07 6.004 6.004 0 0 1 3.431-5.142 3.999 3.999 0 1 1 5.123 0ZM10.5 5a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z"/></svg>
						プロフィール
					</a>
					
						<a class="item" href="/hd-dev-user01?tab=stars">
							<svg viewBox="0 0 16 16" class="svg octicon-star" aria-hidden="true" width="16" height="16"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"/></svg>
							スター
						</a>
					
					<a class="item" href="/notifications/subscriptions">
						<svg viewBox="0 0 16 16" class="svg octicon-bell" aria-hidden="true" width="16" height="16"><path d="M8 16a2 2 0 0 0 1.985-1.75c.017-.137-.097-.25-.235-.25h-3.5c-.138 0-.252.113-.235.25A2 2 0 0 0 8 16ZM3 5a5 5 0 0 1 10 0v2.947c0 .05.015.098.042.139l1.703 2.555A1.519 1.519 0 0 1 13.482 13H2.518a1.516 1.516 0 0 1-1.263-2.36l1.703-2.554A.255.255 0 0 0 3 7.947Zm5-3.5A3.5 3.5 0 0 0 4.5 5v2.947c0 .346-.102.683-.294.97l-1.703 2.556a.017.017 0 0 0-.003.01l.001.006c0 .002.002.004.004.006l.006.004.007.001h10.964l.007-.001.006-.004.004-.006.001-.007a.017.017 0 0 0-.003-.01l-1.703-2.554a1.745 1.745 0 0 1-.294-.97V5A3.5 3.5 0 0 0 8 1.5Z"/></svg>
						購読
					</a>
					<a class="item" href="/user/settings">
						<svg viewBox="0 0 16 16" class="svg octicon-tools" aria-hidden="true" width="16" height="16"><path d="M5.433 2.304A4.492 4.492 0 0 0 3.5 6c0 1.598.832 3.002 2.09 3.802.518.328.929.923.902 1.64v.008l-.164 3.337a.75.75 0 1 1-1.498-.073l.163-3.33c.002-.085-.05-.216-.207-.316A5.996 5.996 0 0 1 2 6a5.993 5.993 0 0 1 2.567-4.92 1.482 1.482 0 0 1 1.673-.04c.462.296.76.827.76 1.423v2.82c0 .082.041.16.11.206l.75.51a.25.25 0 0 0 .28 0l.75-.51A.249.249 0 0 0 9 5.282V2.463c0-.596.298-1.127.76-1.423a1.482 1.482 0 0 1 1.673.04A5.993 5.993 0 0 1 14 6a5.996 5.996 0 0 1-2.786 5.068c-.157.1-.209.23-.207.315l.163 3.33a.752.752 0 0 1-1.094.714.75.75 0 0 1-.404-.64l-.164-3.345c-.027-.717.384-1.312.902-1.64A4.495 4.495 0 0 0 12.5 6a4.492 4.492 0 0 0-1.933-3.696c-.024.017-.067.067-.067.16v2.818a1.75 1.75 0 0 1-.767 1.448l-.75.51a1.75 1.75 0 0 1-1.966 0l-.75-.51A1.75 1.75 0 0 1 5.5 5.282V2.463c0-.092-.043-.142-.067-.159Z"/></svg>
						設定
					</a>
					<a class="item" target="_blank" rel="noopener noreferrer" href="https://docs.gitea.com">
						<svg viewBox="0 0 16 16" class="svg octicon-question" aria-hidden="true" width="16" height="16"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.92 6.085h.001a.749.749 0 1 1-1.342-.67c.169-.339.436-.701.849-.977C6.845 4.16 7.369 4 8 4a2.756 2.756 0 0 1 1.637.525c.503.377.863.965.863 1.725 0 .448-.115.83-.329 1.15-.205.307-.47.513-.692.662-.109.072-.22.138-.313.195l-.006.004a6.24 6.24 0 0 0-.26.16.952.952 0 0 0-.276.245.75.75 0 0 1-1.248-.832c.184-.264.42-.489.692-.661.103-.067.207-.132.313-.195l.007-.004c.1-.061.182-.11.258-.161a.969.969 0 0 0 .277-.245C8.96 6.514 9 6.427 9 6.25a.612.612 0 0 0-.262-.525A1.27 1.27 0 0 0 8 5.5c-.369 0-.595.09-.74.187a1.01 1.01 0 0 0-.34.398ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"/></svg>
						ヘルプ
					</a>
					
						<div class="divider"></div>

						<a class="item" href="/admin">
							<svg viewBox="0 0 16 16" class="svg octicon-server" aria-hidden="true" width="16" height="16"><path d="M1.75 1h12.5c.966 0 1.75.784 1.75 1.75v4c0 .372-.116.717-.314 1 .198.283.314.628.314 1v4a1.75 1.75 0 0 1-1.75 1.75H1.75A1.75 1.75 0 0 1 0 12.75v-4c0-.358.109-.707.314-1a1.739 1.739 0 0 1-.314-1v-4C0 1.784.784 1 1.75 1ZM1.5 2.75v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Zm.25 5.75a.25.25 0 0 0-.25.25v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25ZM7 4.75A.75.75 0 0 1 7.75 4h4.5a.75.75 0 0 1 0 1.5h-4.5A.75.75 0 0 1 7 4.75ZM7.75 10h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM3 4.75A.75.75 0 0 1 3.75 4h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 4.75ZM3.75 10h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"/></svg>
							サイト管理
						</a>
					

					<div class="divider"></div>
					<a class="item link-action" href data-url="/user/logout">
						<svg viewBox="0 0 16 16" class="svg octicon-sign-out" aria-hidden="true" width="16" height="16"><path d="M2 2.75C2 1.784 2.784 1 3.75 1h2.5a.75.75 0 0 1 0 1.5h-2.5a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h2.5a.75.75 0 0 1 0 1.5h-2.5A1.75 1.75 0 0 1 2 13.25Zm10.44 4.5-1.97-1.97a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l3.25 3.25a.75.75 0 0 1 0 1.06l-3.25 3.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734l1.97-1.97H6.75a.75.75 0 0 1 0-1.5Z"/></svg>
						サインアウト
					</a>
				</div>
			</div>
		
	</div>
</nav>

		



<div role="main" aria-label="esg05/register_public_factor.py at 81d9328a5f2a8b9bd976f47f3bd5163081c37afb" class="page-content repository file list ">
	<div class="header-wrapper">

	<div class="ui container">
		<div class="repo-header">
			<div class="repo-title-wrap gt-df gt-fc">
				<div class="repo-title" role="heading" aria-level="1">
					<div class="gt-mr-3">
						

	<svg viewBox="0 0 16 16" class="svg octicon-repo" aria-hidden="true" width="32" height="32"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/></svg>


					</div>
					<a href="/hd-dev-user01">hd-dev-user01</a>
					<div class="gt-mx-2">/</div>
					<a href="/hd-dev-user01/esg05">esg05</a>
					<div class="labels gt-df gt-ac gt-fw">
						
						
							
						
						
					</div>
					
						<a class="rss-icon gt-ml-3" href="/hd-dev-user01/esg05.rss" data-tooltip-content="RSSフィード"><svg viewBox="0 0 16 16" class="svg octicon-rss" aria-hidden="true" width="18" height="18"><path d="M2.002 2.725a.75.75 0 0 1 .797-.699C8.79 2.42 13.58 7.21 13.974 13.201a.75.75 0 0 1-1.497.098 10.502 10.502 0 0 0-9.776-9.776.747.747 0 0 1-.7-.798ZM2.84 7.05h-.002a7.002 7.002 0 0 1 6.113 6.111.75.75 0 0 1-1.49.178 5.503 5.503 0 0 0-4.8-4.8.75.75 0 0 1 .179-1.489ZM2 13a1 1 0 1 1 2 0 1 1 0 0 1-2 0Z"/></svg></a>
					
				</div>
				
				
				
			</div>
			
				<div class="repo-buttons">
					
					<form method="post" action="/hd-dev-user01/esg05/action/unwatch?redirect_to=%2fhd-dev-user01%2fesg05%2fsrc%2fcommit%2f81d9328a5f2a8b9bd976f47f3bd5163081c37afb%2fdags%2fmiddle%2freport_register%2fregister_public_factor.py">
						<input type="hidden" name="_csrf" value="2z24Lq7Pf1CO6d8N4oP2T25w50Y6MTc1MTYyMjM2MTcxMzQ0NzkwOQ">
						<div class="ui labeled button" >
							<button type="submit" class="ui compact small basic button">
								<svg viewBox="0 0 16 16" class="svg octicon-eye-closed" aria-hidden="true" width="16" height="16"><path d="M.143 2.31a.75.75 0 0 1 1.047-.167l14.5 10.5a.75.75 0 1 1-.88 1.214l-2.248-1.628C11.346 13.19 9.792 14 8 14c-1.981 0-3.67-.992-4.933-2.078C1.797 10.832.88 9.577.43 8.9a1.619 1.619 0 0 1 0-1.797c.353-.533.995-1.42 1.868-2.305L.31 3.357A.75.75 0 0 1 .143 2.31Zm1.536 5.622A.12.12 0 0 0 1.657 8c0 .021.006.045.022.068.412.621 1.242 1.75 2.366 2.717C5.175 11.758 6.527 12.5 8 12.5c1.195 0 2.31-.488 3.29-1.191L9.063 9.695A2 2 0 0 1 6.058 7.52L3.529 5.688a14.207 14.207 0 0 0-1.85 2.244ZM8 3.5c-.516 0-1.017.09-1.499.251a.75.75 0 1 1-.473-1.423A6.207 6.207 0 0 1 8 2c1.981 0 3.67.992 4.933 2.078 1.27 1.091 2.187 2.345 2.637 3.023a1.62 1.62 0 0 1 0 1.798c-.11.166-.248.365-.41.587a.75.75 0 1 1-1.21-.887c.148-.201.272-.382.371-.53a.119.119 0 0 0 0-.137c-.412-.621-1.242-1.75-2.366-2.717C10.825 4.242 9.473 3.5 8 3.5Z"/></svg>ウォッチ解除
							</button>
							<a class="ui basic label" href="/hd-dev-user01/esg05/watchers">
								1
							</a>
						</div>
					</form>
					
						<form method="post" action="/hd-dev-user01/esg05/action/star?redirect_to=%2fhd-dev-user01%2fesg05%2fsrc%2fcommit%2f81d9328a5f2a8b9bd976f47f3bd5163081c37afb%2fdags%2fmiddle%2freport_register%2fregister_public_factor.py">
							<input type="hidden" name="_csrf" value="2z24Lq7Pf1CO6d8N4oP2T25w50Y6MTc1MTYyMjM2MTcxMzQ0NzkwOQ">
							<div class="ui labeled button" >
								<button type="submit" class="ui compact small basic button">
									<svg viewBox="0 0 16 16" class="svg octicon-star" aria-hidden="true" width="16" height="16"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"/></svg>スター
								</button>
								<a class="ui basic label" href="/hd-dev-user01/esg05/stars">
									0
								</a>
							</div>
						</form>
					
					
						<div class="ui labeled button
							
								disabled
							"
							
								data-tooltip-content="自分が所有しているリポジトリはフォークできません。"
							
						>
							<a class="ui compact small basic button"
								
									
								
							>
								<svg viewBox="0 0 16 16" class="svg octicon-repo-forked" aria-hidden="true" width="16" height="16"><path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"/></svg>フォーク
							</a>
							<div class="ui small modal" id="fork-repo-modal">
								<div class="header">
									esg05 はフォーク済み
								</div>
								<div class="content gt-text-left">
									<div class="ui list">
										
									</div>
									
								</div>
							</div>
							<a class="ui basic label" href="/hd-dev-user01/esg05/forks">
								0
							</a>
						</div>
					
				</div>
			
		</div>
	</div>

	<div class="ui tabs container">
		
			<div class="ui tabular menu navbar gt-overflow-x-auto gt-overflow-y-hidden">
				
				<a class="active item" href="/hd-dev-user01/esg05">
					<svg viewBox="0 0 16 16" class="svg octicon-code" aria-hidden="true" width="16" height="16"><path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"/></svg> コード
				</a>
				

				
					<a class="item" href="/hd-dev-user01/esg05/issues">
						<svg viewBox="0 0 16 16" class="svg octicon-issue-opened" aria-hidden="true" width="16" height="16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg> イシュー
						
					</a>
				

				

				
					<a class="item" href="/hd-dev-user01/esg05/pulls">
						<svg viewBox="0 0 16 16" class="svg octicon-git-pull-request" aria-hidden="true" width="16" height="16"><path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z"/></svg> プルリクエスト
						
					</a>
				

				

				
					<a href="/hd-dev-user01/esg05/packages" class="item">
						<svg viewBox="0 0 16 16" class="svg octicon-package" aria-hidden="true" width="16" height="16"><path d="m8.878.392 5.25 3.045c.54.314.872.89.872 1.514v6.098a1.75 1.75 0 0 1-.872 1.514l-5.25 3.045a1.75 1.75 0 0 1-1.756 0l-5.25-3.045A1.75 1.75 0 0 1 1 11.049V4.951c0-.624.332-1.201.872-1.514L7.122.392a1.75 1.75 0 0 1 1.756 0ZM7.875 1.69l-4.63 2.685L8 7.133l4.755-2.758-4.63-2.685a.248.248 0 0 0-.25 0ZM2.5 5.677v5.372c0 .09.047.171.125.216l4.625 2.683V8.432Zm6.25 8.271 4.625-2.683a.25.25 0 0 0 .125-.216V5.677L8.75 8.432Z"/></svg> パッケージ
					</a>
				

				
					<a href="/hd-dev-user01/esg05/projects" class="item">
						<svg viewBox="0 0 16 16" class="svg octicon-project" aria-hidden="true" width="16" height="16"><path d="M1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0ZM1.5 1.75v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25ZM11.75 3a.75.75 0 0 1 .75.75v7.5a.75.75 0 0 1-1.5 0v-7.5a.75.75 0 0 1 .75-.75Zm-8.25.75a.75.75 0 0 1 1.5 0v5.5a.75.75 0 0 1-1.5 0ZM8 3a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 3Z"/></svg> プロジェクト
						
					</a>
				

				
				<a class="item" href="/hd-dev-user01/esg05/releases">
					<svg viewBox="0 0 16 16" class="svg octicon-tag" aria-hidden="true" width="16" height="16"><path d="M1 7.775V2.75C1 1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 0 1 0 2.474l-5.026 5.026a1.75 1.75 0 0 1-2.474 0l-6.25-6.25A1.752 1.752 0 0 1 1 7.775Zm1.5 0c0 .066.026.13.073.177l6.25 6.25a.25.25 0 0 0 .354 0l5.025-5.025a.25.25 0 0 0 0-.354l-6.25-6.25a.25.25 0 0 0-.177-.073H2.75a.25.25 0 0 0-.25.25ZM6 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z"/></svg> リリース
					
				</a>
				

				
					<a class="item" href="/hd-dev-user01/esg05/wiki">
						<svg viewBox="0 0 16 16" class="svg octicon-book" aria-hidden="true" width="16" height="16"><path d="M0 1.75A.75.75 0 0 1 .75 1h4.253c1.227 0 2.317.59 3 1.501A3.743 3.743 0 0 1 11.006 1h4.245a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-.75.75h-4.507a2.25 2.25 0 0 0-1.591.659l-.622.621a.75.75 0 0 1-1.06 0l-.622-.621A2.25 2.25 0 0 0 5.258 13H.75a.75.75 0 0 1-.75-.75Zm7.251 10.324.004-5.073-.002-2.253A2.25 2.25 0 0 0 5.003 2.5H1.5v9h3.757a3.75 3.75 0 0 1 1.994.574ZM8.755 4.75l-.004 7.322a3.752 3.752 0 0 1 1.992-.572H14.5v-9h-3.495a2.25 2.25 0 0 0-2.25 2.25Z"/></svg> Wiki
					</a>
				

				

				
					<a class="item" href="/hd-dev-user01/esg05/activity">
						<svg viewBox="0 0 16 16" class="svg octicon-pulse" aria-hidden="true" width="16" height="16"><path d="M6 2c.306 0 .582.187.696.471L10 10.731l1.304-3.26A.751.751 0 0 1 12 7h3.25a.75.75 0 0 1 0 1.5h-2.742l-1.812 4.528a.751.751 0 0 1-1.392 0L6 4.77 4.696 8.03A.75.75 0 0 1 4 8.5H.75a.75.75 0 0 1 0-1.5h2.742l1.812-4.529A.751.751 0 0 1 6 2Z"/></svg> アクティビティ
					</a>
				

				

				
					<a class="right item" href="/hd-dev-user01/esg05/settings">
						<svg viewBox="0 0 16 16" class="svg octicon-tools" aria-hidden="true" width="16" height="16"><path d="M5.433 2.304A4.492 4.492 0 0 0 3.5 6c0 1.598.832 3.002 2.09 3.802.518.328.929.923.902 1.64v.008l-.164 3.337a.75.75 0 1 1-1.498-.073l.163-3.33c.002-.085-.05-.216-.207-.316A5.996 5.996 0 0 1 2 6a5.993 5.993 0 0 1 2.567-4.92 1.482 1.482 0 0 1 1.673-.04c.462.296.76.827.76 1.423v2.82c0 .082.041.16.11.206l.75.51a.25.25 0 0 0 .28 0l.75-.51A.249.249 0 0 0 9 5.282V2.463c0-.596.298-1.127.76-1.423a1.482 1.482 0 0 1 1.673.04A5.993 5.993 0 0 1 14 6a5.996 5.996 0 0 1-2.786 5.068c-.157.1-.209.23-.207.315l.163 3.33a.752.752 0 0 1-1.094.714.75.75 0 0 1-.404-.64l-.164-3.345c-.027-.717.384-1.312.902-1.64A4.495 4.495 0 0 0 12.5 6a4.492 4.492 0 0 0-1.933-3.696c-.024.017-.067.067-.067.16v2.818a1.75 1.75 0 0 1-.767 1.448l-.75.51a1.75 1.75 0 0 1-1.966 0l-.75-.51A1.75 1.75 0 0 1 5.5 5.282V2.463c0-.092-.043-.142-.067-.159Z"/></svg> 設定
					</a>
				
			</div>
		
	</div>
	<div class="ui tabs divider"></div>
</div>

	<div class="ui container ">
		




		

		
		
		<div class="ui form gt-hidden gt-df gt-mt-4" id="topic_edit">
			<div class="field gt-f1 gt-mr-3">
				<div class="ui fluid multiple search selection dropdown" data-text-count-prompt="選択できるのは25トピックまでです。" data-text-format-prompt="トピック名は英字または数字で始め、ダッシュ(&#39;-&#39;)やドット(&#39;.&#39;)を含めることができます。最大35文字までです。文字は小文字でなければなりません。">
					<input type="hidden" name="topics" value="">
					
					<div class="text"></div>
				</div>
			</div>
			<div>
				<button class="ui basic button" id="cancel_topic_edit">キャンセル</button>
				<button class="ui primary button" id="save_topic" data-link="/hd-dev-user01/esg05/topics">保存</button>
			</div>
		</div>
		
		
		

		<div class="repo-button-row">
			<div class="gt-df gt-ac gt-fw gt-gap-y-3">
				






	




<script type="module">
	const data = {
		'textReleaseCompare': "比較",
		'textCreateTag': "タグ \u003cstrong\u003e%s\u003c/strong\u003e を作成",
		'textCreateBranch': "ブランチ \u003cstrong\u003e%s\u003c/strong\u003e を作成",
		'textCreateBranchFrom': "\"%s\" から",
		'textBranches': "ブランチ",
		'textTags': "タグ",
		'textDefaultBranchLabel': "デフォルト",

		'mode': 'branches',
		'showBranchesInDropdown':  true ,
		'searchFieldPlaceholder': 'ブランチまたはタグを絞り込み...',
		'branchForm':  null ,
		'disableCreateBranch':  false ,
		'setAction':  null ,
		'submitForm':  null ,
		'viewType': "tree",
		'refName': "81d9328a5f",
		'commitIdShort': "81d9328a5f",
		'tagName': "",
		'branchName': "main",
		'noTag':  null ,
		'defaultSelectedRefName': "main",
		'repoDefaultBranch': "main",
		'enableFeed':  true ,
		'rssURLPrefix': '\/hd-dev-user01\/esg05/rss/branch/',
		'branchURLPrefix': '\/hd-dev-user01\/esg05/src/branch/',
		'branchURLSuffix': '/dags\/middle\/report_register\/register_public_factor.py',
		'tagURLPrefix': '\/hd-dev-user01\/esg05/src/tag/',
		'tagURLSuffix': '/dags\/middle\/report_register\/register_public_factor.py',
		'repoLink': "/hd-dev-user01/esg05",
		'treePath': "dags/middle/report_register/register_public_factor.py",
		'branchNameSubURL': "commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb",
		'noResults': "結果が見つかりませんでした。",
	};
	
	window.config.pageData.branchDropdownDataList = window.config.pageData.branchDropdownDataList || [];
	window.config.pageData.branchDropdownDataList.push(data);
</script>

<div class="js-branch-tag-selector gt-mr-2">
	
	<div class="ui dropdown custom">
		<button class="branch-dropdown-button gt-ellipsis ui basic small compact button gt-df gt-m-0">
			<span class="text gt-df gt-ac gt-mr-2">
				
					
						<svg viewBox="0 0 16 16" class="svg octicon-git-branch" aria-hidden="true" width="16" height="16"><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"/></svg>
					
					<strong ref="dropdownRefName" class="gt-ml-3">81d9328a5f</strong>
				
			</span>
			<svg viewBox="0 0 16 16" class="dropdown icon svg octicon-triangle-down" aria-hidden="true" width="14" height="14"><path d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427Z"/></svg>
		</button>
	</div>
</div>

				
				
				
				
				

				

				
				
					<span class="breadcrumb repo-path gt-ml-2">
						<a class="section" href="/hd-dev-user01/esg05/src/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb" title="esg05">esg05</a><span class="breadcrumb-divider">/</span><span class="section"><a href="/hd-dev-user01/esg05/src/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags" title="dags">dags</a></span><span class="breadcrumb-divider">/</span><span class="section"><a href="/hd-dev-user01/esg05/src/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle" title="middle">middle</a></span><span class="breadcrumb-divider">/</span><span class="section"><a href="/hd-dev-user01/esg05/src/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register" title="report_register">report_register</a></span><span class="breadcrumb-divider">/</span><span class="active section" title="register_public_factor.py">register_public_factor.py</span></span>
				
			</div>
			<div class="gt-df gt-ac">
				
				
				
			</div>
		</div>
		
			<div class="tab-size-4 non-diff-file-content">
	<h4 class="file-header ui top attached header gt-df gt-ac gt-sb gt-fw">
		<div class="file-header-left gt-df gt-ac gt-py-3 gt-pr-4">
			
				<div class="file-info text grey normal gt-mono">
	
	
		<div class="file-info-entry">
			524 行
		</div>
	
	
		<div class="file-info-entry">
			24 KiB
		</div>
	
	
	
		<div class="file-info-entry">
			Python
		</div>
	
	
	
</div>

			
		</div>
		<div class="file-header-right file-actions gt-df gt-ac gt-fw">
			
			
				<div class="ui buttons gt-mr-2">
					<a class="ui mini basic button" href="/hd-dev-user01/esg05/raw/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py">Raw</a>
					
					
						<a class="ui mini basic button" href="/hd-dev-user01/esg05/blame/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py">Blame</a>
					
					<a class="ui mini basic button" href="/hd-dev-user01/esg05/commits/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py">履歴</a>
					
						<button class="ui mini basic button unescape-button gt-hidden">エスケープ解除</button>
						<button class="ui mini basic button escape-button">エスケープ</button>
					
				</div>
				<a download href="/hd-dev-user01/esg05/raw/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py"><span class="btn-octicon" data-tooltip-content="ファイルをダウンロード"><svg viewBox="0 0 16 16" class="svg octicon-download" aria-hidden="true" width="16" height="16"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-2.5a.75.75 0 0 1 1.5 0v2.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 1.5 0v2.5A1.75 1.75 0 0 1 13.25 14Z"/><path d="M7.25 7.689V2a.75.75 0 0 1 1.5 0v5.689l1.97-1.969a.749.749 0 1 1 1.06 1.06l-3.25 3.25a.749.749 0 0 1-1.06 0L4.22 6.78a.749.749 0 1 1 1.06-1.06l1.97 1.969Z"/></svg></span></a>
				<a id="copy-content" class="btn-octicon " data-tooltip-content="内容をコピー"><svg viewBox="0 0 16 16" class="svg octicon-copy" aria-hidden="true" width="14" height="14"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"/><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg></a>
				
				<a class="btn-octicon" href="/hd-dev-user01/esg05/rss/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py"><svg viewBox="0 0 16 16" class="svg octicon-rss" aria-hidden="true" width="14" height="14"><path d="M2.002 2.725a.75.75 0 0 1 .797-.699C8.79 2.42 13.58 7.21 13.974 13.201a.75.75 0 0 1-1.497.098 10.502 10.502 0 0 0-9.776-9.776.747.747 0 0 1-.7-.798ZM2.84 7.05h-.002a7.002 7.002 0 0 1 6.113 6.111.75.75 0 0 1-1.49.178 5.503 5.503 0 0 0-4.8-4.8.75.75 0 0 1 .179-1.489ZM2 13a1 1 0 1 1 2 0 1 1 0 0 1-2 0Z"/></svg></a>
				
				
					
						<span class="btn-octicon disabled" data-tooltip-content="このファイルを変更したり変更の提案をするには、ブランチ上にいる必要があります。"><svg viewBox="0 0 16 16" class="svg octicon-pencil" aria-hidden="true" width="16" height="16"><path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z"/></svg></span>
					
					
						<span class="btn-octicon disabled" data-tooltip-content="このファイルを変更したり変更の提案をするには、ブランチ上にいる必要があります。"><svg viewBox="0 0 16 16" class="svg octicon-trash" aria-hidden="true" width="16" height="16"><path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"/></svg></span>
					
				
			
		</div>
	</h4>
	<div class="ui attached table unstackable segment">
		
			
	
		<div class="ui warning message unicode-escape-prompt gt-text-left">
			<button class="close icon hide-panel button" data-panel-closest=".message"><svg viewBox="0 0 16 16" class="close inside svg octicon-x" aria-hidden="true" width="16" height="16"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"/></svg></button>
			<div class="header">
				このファイルには不可視のUnicode文字が含まれています
			</div>
			<p>このファイルには人間が識別できない不可視のUnicode文字が含まれており、コンピューターによって特殊な処理が行われる可能性があります。 それが意図的なものと考えられる場合は、この警告を無視して構いません。 不可視文字を表示するにはエスケープボタンを使用します。</p>
			
		</div>
	


		
		<div class="file-view code-view">
			
				
				<table>
					<tbody>
						
						
						<tr>
							<td id="L1" class="lines-num"><span id="L1" data-line-number="1"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L1" class="lines-code chroma"><code class="code-inner"><span class="kn">import</span> <span class="nn">re</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L2" class="lines-num"><span id="L2" data-line-number="2"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L2" class="lines-code chroma"><code class="code-inner"><span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L3" class="lines-num"><span id="L3" data-line-number="3"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L3" class="lines-code chroma"><code class="code-inner"><span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L4" class="lines-num"><span id="L4" data-line-number="4"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L4" class="lines-code chroma"><code class="code-inner"><span class="kn">import</span> <span class="nn">os</span><span class="o">,</span> <span class="nn">traceback</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L5" class="lines-num"><span id="L5" data-line-number="5"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L5" class="lines-code chroma"><code class="code-inner"><span class="kn">from</span> <span class="nn">pyhive</span><span class="nn">.</span><span class="nn">exc</span> <span class="kn">import</span> <span class="n">DatabaseError</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L6" class="lines-num"><span id="L6" data-line-number="6"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L6" class="lines-code chroma"><code class="code-inner"><span class="kn">from</span> <span class="nn">airflow</span><span class="nn">.</span><span class="nn">models</span> <span class="kn">import</span> <span class="n">Variable</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L7" class="lines-num"><span id="L7" data-line-number="7"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L7" class="lines-code chroma"><code class="code-inner"><span class="kn">from</span> <span class="nn">middle</span><span class="nn">.</span><span class="nn">common</span><span class="nn">.</span><span class="nn">postgre_connect</span> <span class="kn">import</span> <span class="n">Psycopg2Singleton</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L8" class="lines-num"><span id="L8" data-line-number="8"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L8" class="lines-code chroma"><code class="code-inner"><span class="kn">import</span> <span class="nn">middle</span><span class="nn">.</span><span class="nn">common</span><span class="nn">.</span><span class="nn">utils</span> <span class="k">as</span> <span class="nn">utils</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L9" class="lines-num"><span id="L9" data-line-number="9"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L9" class="lines-code chroma"><code class="code-inner"><span class="kn">import</span> <span class="nn">middle</span><span class="nn">.</span><span class="nn">common</span><span class="nn">.</span><span class="nn">log</span> <span class="k">as</span> <span class="nn">log</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L10" class="lines-num"><span id="L10" data-line-number="10"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L10" class="lines-code chroma"><code class="code-inner"><span class="kn">import</span> <span class="nn">middle</span><span class="nn">.</span><span class="nn">common</span><span class="nn">.</span><span class="nn">constants_colums</span> <span class="k">as</span> <span class="nn">constants</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L11" class="lines-num"><span id="L11" data-line-number="11"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L11" class="lines-code chroma"><code class="code-inner"><span class="kn">from</span> <span class="nn">middle</span><span class="nn">.</span><span class="nn">common</span><span class="nn">.</span><span class="nn">hive_connect</span> <span class="kn">import</span> <span class="n">ImpalaSingleton</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L12" class="lines-num"><span id="L12" data-line-number="12"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L12" class="lines-code chroma"><code class="code-inner"><span class="kn">from</span> <span class="nn">middle</span><span class="nn">.</span><span class="nn">common</span><span class="nn">.</span><span class="nn">hql_processor</span> <span class="kn">import</span> <span class="n">execute_delete</span><span class="p">,</span> <span class="n">execute_hive_update</span><span class="p">,</span> <span class="n">execute_insert</span><span class="p">,</span> <span class="n">execute_update</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L13" class="lines-num"><span id="L13" data-line-number="13"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L13" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L14" class="lines-num"><span id="L14" data-line-number="14"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L14" class="lines-code chroma"><code class="code-inner"><span class="c1"># loogerオブジェクト取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L15" class="lines-num"><span id="L15" data-line-number="15"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L15" class="lines-code chroma"><code class="code-inner"><span class="n">logger</span> <span class="o">=</span> <span class="n">log</span><span class="o">.</span><span class="n">MiddleAppLog</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L16" class="lines-num"><span id="L16" data-line-number="16"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L16" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L17" class="lines-num"><span id="L17" data-line-number="17"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L17" class="lines-code chroma"><code class="code-inner"><span class="c1"># &#34;.&#34; &#34;&#34; &#34;-&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L18" class="lines-num"><span id="L18" data-line-number="18"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L18" class="lines-code chroma"><code class="code-inner"><span class="n">DOT</span> <span class="o">=</span> <span class="n">constants</span><span class="o">.</span><span class="n">SpecialChars</span><span class="o">.</span><span class="n">DOT</span><span class="o">.</span><span class="n">value</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L19" class="lines-num"><span id="L19" data-line-number="19"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L19" class="lines-code chroma"><code class="code-inner"><span class="n">BLANK</span> <span class="o">=</span> <span class="n">constants</span><span class="o">.</span><span class="n">SpecialChars</span><span class="o">.</span><span class="n">BLANK</span><span class="o">.</span><span class="n">value</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L20" class="lines-num"><span id="L20" data-line-number="20"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L20" class="lines-code chroma"><code class="code-inner"><span class="n">HYPHEN</span> <span class="o">=</span> <span class="n">constants</span><span class="o">.</span><span class="n">SpecialChars</span><span class="o">.</span><span class="n">HYPHEN</span><span class="o">.</span><span class="n">value</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L21" class="lines-num"><span id="L21" data-line-number="21"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L21" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L22" class="lines-num"><span id="L22" data-line-number="22"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L22" class="lines-code chroma"><code class="code-inner"><span class="c1"># システム操作時タイムスタンプ取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L23" class="lines-num"><span id="L23" data-line-number="23"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L23" class="lines-code chroma"><code class="code-inner"><span class="n">current_timestamp</span> <span class="o">=</span> <span class="n">utils</span><span class="o">.</span><span class="n">get_current_timestamp</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L24" class="lines-num"><span id="L24" data-line-number="24"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L24" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L25" class="lines-num"><span id="L25" data-line-number="25"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L25" class="lines-code chroma"><code class="code-inner"><span class="c1"># データ登録処理実行者</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L26" class="lines-num"><span id="L26" data-line-number="26"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L26" class="lines-code chroma"><code class="code-inner"><span class="n">creator_name</span> <span class="o">=</span> <span class="n">utils</span><span class="o">.</span><span class="n">get_sysuser</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L27" class="lines-num"><span id="L27" data-line-number="27"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L27" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L28" class="lines-num"><span id="L28" data-line-number="28"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L28" class="lines-code chroma"><code class="code-inner"><span class="c1"># データベース名取得する</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L29" class="lines-num"><span id="L29" data-line-number="29"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L29" class="lines-code chroma"><code class="code-inner"><span class="n">json_config</span> <span class="o">=</span> <span class="n">utils</span><span class="o">.</span><span class="n">get_json_config</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L30" class="lines-num"><span id="L30" data-line-number="30"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L30" class="lines-code chroma"><code class="code-inner"><span class="n">schema_commom</span> <span class="o">=</span> <span class="n">json_config</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">database_posgre</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">schema_commom</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L31" class="lines-num"><span id="L31" data-line-number="31"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L31" class="lines-code chroma"><code class="code-inner"><span class="n">schema_middle</span> <span class="o">=</span> <span class="n">json_config</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">database_posgre</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">schema_middle</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L32" class="lines-num"><span id="L32" data-line-number="32"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L32" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L33" class="lines-num"><span id="L33" data-line-number="33"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L33" class="lines-code chroma"><code class="code-inner"><span class="n">hive_common_user</span> <span class="o">=</span> <span class="n">json_config</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">hive_common</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">user</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L34" class="lines-num"><span id="L34" data-line-number="34"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L34" class="lines-code chroma"><code class="code-inner"><span class="n">hive_common_password</span> <span class="o">=</span> <span class="n">json_config</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">hive_common</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">password</span><span class="s2">&#34;</span><span class="p">]</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L35" class="lines-num"><span id="L35" data-line-number="35"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L35" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L36" class="lines-num"><span id="L36" data-line-number="36"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L36" class="lines-code chroma"><code class="code-inner"><span class="n">hive_corp_user</span> <span class="o">=</span> <span class="n">json_config</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">database_hive</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">user</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L37" class="lines-num"><span id="L37" data-line-number="37"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L37" class="lines-code chroma"><code class="code-inner"><span class="n">hive_corp_password</span> <span class="o">=</span> <span class="n">json_config</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">database_hive</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">password</span><span class="s2">&#34;</span><span class="p">]</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L38" class="lines-num"><span id="L38" data-line-number="38"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L38" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L39" class="lines-num"><span id="L39" data-line-number="39"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L39" class="lines-code chroma"><code class="code-inner"><span class="c1"># rootパス取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L40" class="lines-num"><span id="L40" data-line-number="40"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L40" class="lines-code chroma"><code class="code-inner"><span class="n">project_root_path</span> <span class="o">=</span> <span class="n">utils</span><span class="o">.</span><span class="n">get_project_root_path</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L41" class="lines-num"><span id="L41" data-line-number="41"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L41" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L42" class="lines-num"><span id="L42" data-line-number="42"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L42" class="lines-code chroma"><code class="code-inner"><span class="nd">@log.log_writer</span><span class="p">(</span><span class="n">logger</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L43" class="lines-num"><span id="L43" data-line-number="43"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L43" class="lines-code chroma"><code class="code-inner"><span class="k">def</span> <span class="nf">insert_public_factor</span><span class="p">(</span><span class="n">target_sheets</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">*</span><span class="o">*</span><span class="n">kwargs</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L44" class="lines-num"><span id="L44" data-line-number="44"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L44" class="lines-code chroma"><code class="code-inner">    <span class="sa"></span><span class="s2">&#34;&#34;&#34;</span><span class="s2">指定された公的係数のシートをDWHへ登録する</span><span class="s2">&#34;&#34;&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L45" class="lines-num"><span id="L45" data-line-number="45"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L45" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L46" class="lines-num"><span id="L46" data-line-number="46"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L46" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 実行モード取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L47" class="lines-num"><span id="L47" data-line-number="47"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L47" class="lines-code chroma"><code class="code-inner">    <span class="n">run_mode</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">MIDDLE_RUN_MODE</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">constants</span><span class="o">.</span><span class="n">RunMode</span><span class="o">.</span><span class="n">DEV</span><span class="o">.</span><span class="n">value</span><span class="p">)</span> \
</code></td>
						</tr>
						
						
						<tr>
							<td id="L48" class="lines-num"><span id="L48" data-line-number="48"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L48" class="lines-code chroma"><code class="code-inner">        <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">MIDDLE_RUN_MODE</span><span class="s2">&#34;</span><span class="p">)</span> <span class="ow">is</span> <span class="kc">None</span> <span class="k">else</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">MIDDLE_RUN_MODE</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L49" class="lines-num"><span id="L49" data-line-number="49"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L49" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L50" class="lines-num"><span id="L50" data-line-number="50"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L50" class="lines-code chroma"><code class="code-inner">    <span class="c1"># excelファイル処理用ライブラリopenpyxlをインストール</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L51" class="lines-num"><span id="L51" data-line-number="51"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L51" class="lines-code chroma"><code class="code-inner">    <span class="n">utils</span><span class="o">.</span><span class="n">install_package</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">openpyxl</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L52" class="lines-num"><span id="L52" data-line-number="52"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L52" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L53" class="lines-num"><span id="L53" data-line-number="53"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L53" class="lines-code chroma"><code class="code-inner">    <span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">★★★公的係数の登録処理を開始します★★★</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L54" class="lines-num"><span id="L54" data-line-number="54"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L54" class="lines-code chroma"><code class="code-inner">    <span class="c1"># hive接続インスタンス</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L55" class="lines-num"><span id="L55" data-line-number="55"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L55" class="lines-code chroma"><code class="code-inner">    <span class="n">hive_common_connect_singleton</span> <span class="o">=</span> <span class="n">common_conn</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L56" class="lines-num"><span id="L56" data-line-number="56"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L56" class="lines-code chroma"><code class="code-inner">    <span class="n">hive_corp_connect_singleton</span> <span class="o">=</span> <span class="n">corp_conn</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L57" class="lines-num"><span id="L57" data-line-number="57"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L57" class="lines-code chroma"><code class="code-inner">    <span class="n">postgre_connect_singleton</span> <span class="o">=</span> <span class="n">postgre_conn</span> <span class="o">=</span> <span class="kc">None</span>  <span class="c1"># postgre接続インスタンス</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L58" class="lines-num"><span id="L58" data-line-number="58"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L58" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L59" class="lines-num"><span id="L59" data-line-number="59"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L59" class="lines-code chroma"><code class="code-inner">    <span class="k">if</span> <span class="n">run_mode</span> <span class="ow">in</span> <span class="p">(</span> <span class="n">constants</span><span class="o">.</span><span class="n">RunMode</span><span class="o">.</span><span class="n">PROD</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">constants</span><span class="o">.</span><span class="n">RunMode</span><span class="o">.</span><span class="n">S2_PROD</span><span class="o">.</span><span class="n">value</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L60" class="lines-num"><span id="L60" data-line-number="60"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L60" class="lines-code chroma"><code class="code-inner">        <span class="c1"># postgre connect接続</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L61" class="lines-num"><span id="L61" data-line-number="61"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L61" class="lines-code chroma"><code class="code-inner">        <span class="n">postgre_connect_singleton</span> <span class="o">=</span> <span class="n">Psycopg2Singleton</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L62" class="lines-num"><span id="L62" data-line-number="62"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L62" class="lines-code chroma"><code class="code-inner">        <span class="c1"># コネクション取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L63" class="lines-num"><span id="L63" data-line-number="63"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L63" class="lines-code chroma"><code class="code-inner">        <span class="n">postgre_conn</span> <span class="o">=</span> <span class="n">postgre_connect_singleton</span><span class="o">.</span><span class="n">_connection</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L64" class="lines-num"><span id="L64" data-line-number="64"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L64" class="lines-code chroma"><code class="code-inner">        <span class="c1"># Hive connect接続</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L65" class="lines-num"><span id="L65" data-line-number="65"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L65" class="lines-code chroma"><code class="code-inner">        <span class="n">hive_common_connect_singleton</span> <span class="o">=</span> <span class="n">ImpalaSingleton</span><span class="p">(</span><span class="n">hive_common_user</span><span class="p">,</span> <span class="n">hive_common_password</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L66" class="lines-num"><span id="L66" data-line-number="66"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L66" class="lines-code chroma"><code class="code-inner">        <span class="c1"># コネクション取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L67" class="lines-num"><span id="L67" data-line-number="67"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L67" class="lines-code chroma"><code class="code-inner">        <span class="n">common_conn</span> <span class="o">=</span> <span class="n">hive_common_connect_singleton</span><span class="o">.</span><span class="n">_connection</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L68" class="lines-num"><span id="L68" data-line-number="68"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L68" class="lines-code chroma"><code class="code-inner">        <span class="c1"># Hive connect接続</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L69" class="lines-num"><span id="L69" data-line-number="69"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L69" class="lines-code chroma"><code class="code-inner">        <span class="n">hive_corp_connect_singleton</span> <span class="o">=</span> <span class="n">ImpalaSingleton</span><span class="p">(</span><span class="n">hive_corp_user</span><span class="p">,</span> <span class="n">hive_corp_password</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L70" class="lines-num"><span id="L70" data-line-number="70"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L70" class="lines-code chroma"><code class="code-inner">        <span class="c1"># コネクション取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L71" class="lines-num"><span id="L71" data-line-number="71"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L71" class="lines-code chroma"><code class="code-inner">        <span class="n">corp_conn</span> <span class="o">=</span> <span class="n">hive_corp_connect_singleton</span><span class="o">.</span><span class="n">_connection</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L72" class="lines-num"><span id="L72" data-line-number="72"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L72" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L73" class="lines-num"><span id="L73" data-line-number="73"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L73" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 処理する入力シートファイル一覧取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L74" class="lines-num"><span id="L74" data-line-number="74"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L74" class="lines-code chroma"><code class="code-inner">    <span class="n">excel_files</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L75" class="lines-num"><span id="L75" data-line-number="75"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L75" class="lines-code chroma"><code class="code-inner">    <span class="k">if</span> <span class="n">run_mode</span> <span class="o">==</span> <span class="n">constants</span><span class="o">.</span><span class="n">RunMode</span><span class="o">.</span><span class="n">DEV</span><span class="o">.</span><span class="n">value</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L76" class="lines-num"><span id="L76" data-line-number="76"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L76" class="lines-code chroma"><code class="code-inner">        <span class="c1"># excel_files = utils.get_files(&#34;masterfiles&#34;)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L77" class="lines-num"><span id="L77" data-line-number="77"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L77" class="lines-code chroma"><code class="code-inner">        <span class="n">excel_files</span> <span class="o">=</span> <span class="p">[</span><span class="sa">r</span><span class="s1">&#39;</span><span class="s1">C:</span><span class="s1">\</span><span class="s1">Users</span><span class="s1">\</span><span class="s1">msduser</span><span class="s1">\</span><span class="s1">cndx_workspace</span><span class="s1">\</span><span class="s1">esg05</span><span class="s1">\</span><span class="s1">dags</span><span class="s1">\</span><span class="s1">middle</span><span class="s1">\</span><span class="s1">files</span><span class="s1">\</span><span class="s1">masterfiles</span><span class="s1">\</span><span class="s1">EEGS_master.xlsx</span><span class="s1">&#39;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L78" class="lines-num"><span id="L78" data-line-number="78"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L78" class="lines-code chroma"><code class="code-inner">    <span class="k">else</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L79" class="lines-num"><span id="L79" data-line-number="79"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L79" class="lines-code chroma"><code class="code-inner">        <span class="n">base_path</span> <span class="o">=</span> <span class="n">Variable</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">middle_download_put_base_path</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L80" class="lines-num"><span id="L80" data-line-number="80"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L80" class="lines-code chroma"><code class="code-inner">        <span class="n">sub_path</span> <span class="o">=</span> <span class="n">Variable</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">middle_download_put_masterfiles_path</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L81" class="lines-num"><span id="L81" data-line-number="81"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L81" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L82" class="lines-num"><span id="L82" data-line-number="82"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L82" class="lines-code chroma"><code class="code-inner">        <span class="c1"># Hadoopから対象ファイルのBytesIOを取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L83" class="lines-num"><span id="L83" data-line-number="83"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L83" class="lines-code chroma"><code class="code-inner">        <span class="n">excel_files</span> <span class="o">=</span> <span class="n">utils</span><span class="o">.</span><span class="n">get_file_from_hadoop</span><span class="p">(</span><span class="n">base_path</span><span class="p">,</span> <span class="n">sub_path</span><span class="p">,</span> <span class="kc">None</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L84" class="lines-num"><span id="L84" data-line-number="84"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L84" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L85" class="lines-num"><span id="L85" data-line-number="85"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L85" class="lines-code chroma"><code class="code-inner">    <span class="c1"># ファイル存在チェック</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L86" class="lines-num"><span id="L86" data-line-number="86"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L86" class="lines-code chroma"><code class="code-inner">    <span class="k">if</span> <span class="p">(</span><span class="n">excel_files</span> <span class="ow">is</span> <span class="kc">None</span> <span class="ow">or</span> <span class="nb">len</span><span class="p">(</span><span class="n">excel_files</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L87" class="lines-num"><span id="L87" data-line-number="87"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L87" class="lines-code chroma"><code class="code-inner">        <span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">登録・更新するファイルがないため、処理を中止します。</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L88" class="lines-num"><span id="L88" data-line-number="88"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L88" class="lines-code chroma"><code class="code-inner">        <span class="k">return</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L89" class="lines-num"><span id="L89" data-line-number="89"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L89" class="lines-code chroma"><code class="code-inner">    
</code></td>
						</tr>
						
						
						<tr>
							<td id="L90" class="lines-num"><span id="L90" data-line-number="90"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L90" class="lines-code chroma"><code class="code-inner">    <span class="c1"># ファイル数分処理を繰り返す読み込み</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L91" class="lines-num"><span id="L91" data-line-number="91"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L91" class="lines-code chroma"><code class="code-inner">    <span class="c1"># for excel_file in excel_files: # 🔥🔥🔥🔥テスト用</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L92" class="lines-num"><span id="L92" data-line-number="92"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L92" class="lines-code chroma"><code class="code-inner">    <span class="k">for</span> <span class="n">file_path</span><span class="p">,</span> <span class="n">excel_file</span> <span class="ow">in</span> <span class="n">excel_files</span><span class="o">.</span><span class="n">items</span><span class="p">(</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L93" class="lines-num"><span id="L93" data-line-number="93"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L93" class="lines-code chroma"><code class="code-inner">        <span class="n">logger</span><span class="o">.</span><span class="n">debug</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;</span><span class="s2">★処理中ファイル名： </span><span class="si">{</span><span class="n">excel_file</span><span class="si">}</span><span class="s2"> ★</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L94" class="lines-num"><span id="L94" data-line-number="94"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L94" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L95" class="lines-num"><span id="L95" data-line-number="95"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L95" class="lines-code chroma"><code class="code-inner">        <span class="k">with</span> <span class="n">pd</span><span class="o">.</span><span class="n">ExcelFile</span><span class="p">(</span><span class="n">excel_file</span><span class="p">)</span> <span class="k">as</span> <span class="n">file</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L96" class="lines-num"><span id="L96" data-line-number="96"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L96" class="lines-code chroma"><code class="code-inner">            <span class="n">sheet_names</span> <span class="o">=</span> <span class="n">file</span><span class="o">.</span><span class="n">sheet_names</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L97" class="lines-num"><span id="L97" data-line-number="97"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L97" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L98" class="lines-num"><span id="L98" data-line-number="98"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L98" class="lines-code chroma"><code class="code-inner">        <span class="k">try</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L99" class="lines-num"><span id="L99" data-line-number="99"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L99" class="lines-code chroma"><code class="code-inner">            <span class="k">if</span> <span class="n">run_mode</span> <span class="o">==</span> <span class="n">constants</span><span class="o">.</span><span class="n">RunMode</span><span class="o">.</span><span class="n">DEV</span><span class="o">.</span><span class="n">value</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L100" class="lines-num"><span id="L100" data-line-number="100"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L100" class="lines-code chroma"><code class="code-inner">                <span class="c1"># industy_classification_df.to_csv(&#34;industy_classification.csv&#34;, index=False)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L101" class="lines-num"><span id="L101" data-line-number="101"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L101" class="lines-code chroma"><code class="code-inner">                <span class="c1"># electric_supplier_menu_df.to_csv(&#34;electric_supplier_menu.csv&#34;, index=False)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L102" class="lines-num"><span id="L102" data-line-number="102"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L102" class="lines-code chroma"><code class="code-inner">                <span class="c1"># activity_minor_category_df.to_csv(&#34;activity_minor_category.csv&#34;, index=False)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L103" class="lines-num"><span id="L103" data-line-number="103"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L103" class="lines-code chroma"><code class="code-inner">                <span class="k">pass</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L104" class="lines-num"><span id="L104" data-line-number="104"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L104" class="lines-code chroma"><code class="code-inner">            <span class="k">else</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L105" class="lines-num"><span id="L105" data-line-number="105"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L105" class="lines-code chroma"><code class="code-inner">                <span class="n">industry_sheet_flg</span> <span class="o">=</span> <span class="kc">False</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L106" class="lines-num"><span id="L106" data-line-number="106"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L106" class="lines-code chroma"><code class="code-inner">                <span class="c1"># シート数分を繰り返す</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L107" class="lines-num"><span id="L107" data-line-number="107"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L107" class="lines-code chroma"><code class="code-inner">                <span class="k">for</span> <span class="n">sheet_name</span> <span class="ow">in</span> <span class="n">sheet_names</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L108" class="lines-num"><span id="L108" data-line-number="108"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L108" class="lines-code chroma"><code class="code-inner">                    <span class="c1"># target_sheetsが指定されている場合、シート名が対象シートに含まれていないとスキップ</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L109" class="lines-num"><span id="L109" data-line-number="109"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L109" class="lines-code chroma"><code class="code-inner">                    <span class="c1"># if target_sheets and sheet_name not in target_sheets:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L110" class="lines-num"><span id="L110" data-line-number="110"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L110" class="lines-code chroma"><code class="code-inner">                    <span class="c1">#     logger.info(f&#34;シート {sheet_name} は指定されていないため、スキップします。&#34;)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L111" class="lines-num"><span id="L111" data-line-number="111"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L111" class="lines-code chroma"><code class="code-inner">                    <span class="c1">#     continue</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L112" class="lines-num"><span id="L112" data-line-number="112"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L112" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L113" class="lines-num"><span id="L113" data-line-number="113"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L113" class="lines-code chroma"><code class="code-inner">                    <span class="k">if</span> <span class="n">constants</span><span class="o">.</span><span class="n">EEGSMasterSheetName</span><span class="o">.</span><span class="n">AMCMST_SHEET_NAME</span><span class="o">.</span><span class="n">value</span> <span class="o">==</span> <span class="n">sheet_name</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L114" class="lines-num"><span id="L114" data-line-number="114"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L114" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_delete</span><span class="p">(</span><span class="n">postgre_conn</span><span class="p">,</span> <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">AMCMST</span><span class="o">.</span><span class="n">value</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L115" class="lines-num"><span id="L115" data-line-number="115"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L115" class="lines-code chroma"><code class="code-inner">                        <span class="n">activity_minor_category_df</span> <span class="o">=</span>  <span class="n">get_activity_minor_category_data</span><span class="p">(</span><span class="n">excel_file</span><span class="p">,</span> <span class="n">sheet_name</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L116" class="lines-num"><span id="L116" data-line-number="116"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L116" class="lines-code chroma"><code class="code-inner">                        <span class="c1"># PostgreS登録</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L117" class="lines-num"><span id="L117" data-line-number="117"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L117" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_insert</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L118" class="lines-num"><span id="L118" data-line-number="118"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L118" class="lines-code chroma"><code class="code-inner">                            <span class="n">postgre_conn</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L119" class="lines-num"><span id="L119" data-line-number="119"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L119" class="lines-code chroma"><code class="code-inner">                            <span class="n">activity_minor_category_df</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L120" class="lines-num"><span id="L120" data-line-number="120"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L120" class="lines-code chroma"><code class="code-inner">                            <span class="n">constants</span><span class="o">.</span><span class="n">AMCMST_COLUMNS</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L121" class="lines-num"><span id="L121" data-line-number="121"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L121" class="lines-code chroma"><code class="code-inner">                            <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">AMCMST</span><span class="o">.</span><span class="n">value</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L122" class="lines-num"><span id="L122" data-line-number="122"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L122" class="lines-code chroma"><code class="code-inner">                        <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L123" class="lines-num"><span id="L123" data-line-number="123"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L123" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L124" class="lines-num"><span id="L124" data-line-number="124"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L124" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_hive_update</span><span class="p">(</span><span class="n">common_conn</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L125" class="lines-num"><span id="L125" data-line-number="125"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L125" class="lines-code chroma"><code class="code-inner">                                            <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">AMCMST</span><span class="o">.</span><span class="n">value</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L126" class="lines-num"><span id="L126" data-line-number="126"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L126" class="lines-code chroma"><code class="code-inner">                                            <span class="n">constants</span><span class="o">.</span><span class="n">AMCMST_COLUMNS</span><span class="p">,</span> <span class="kc">False</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L127" class="lines-num"><span id="L127" data-line-number="127"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L127" class="lines-code chroma"><code class="code-inner">                        <span class="c1"># Hive登録</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L128" class="lines-num"><span id="L128" data-line-number="128"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L128" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_insert</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L129" class="lines-num"><span id="L129" data-line-number="129"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L129" class="lines-code chroma"><code class="code-inner">                            <span class="n">common_conn</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L130" class="lines-num"><span id="L130" data-line-number="130"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L130" class="lines-code chroma"><code class="code-inner">                            <span class="n">activity_minor_category_df</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L131" class="lines-num"><span id="L131" data-line-number="131"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L131" class="lines-code chroma"><code class="code-inner">                            <span class="n">constants</span><span class="o">.</span><span class="n">AMCMST_COLUMNS</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L132" class="lines-num"><span id="L132" data-line-number="132"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L132" class="lines-code chroma"><code class="code-inner">                            <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">AMCMST</span><span class="o">.</span><span class="n">value</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L133" class="lines-num"><span id="L133" data-line-number="133"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L133" class="lines-code chroma"><code class="code-inner">                        <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L134" class="lines-num"><span id="L134" data-line-number="134"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L134" class="lines-code chroma"><code class="code-inner">                    <span class="k">if</span> <span class="n">constants</span><span class="o">.</span><span class="n">EEGSMasterSheetName</span><span class="o">.</span><span class="n">MECF_SHEET_NAME</span><span class="o">.</span><span class="n">value</span> <span class="o">==</span> <span class="n">sheet_name</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L135" class="lines-num"><span id="L135" data-line-number="135"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L135" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_delete</span><span class="p">(</span><span class="n">postgre_conn</span><span class="p">,</span> <span class="n">schema_middle</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MECF</span><span class="o">.</span><span class="n">value</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L136" class="lines-num"><span id="L136" data-line-number="136"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L136" class="lines-code chroma"><code class="code-inner">                        <span class="n">electric_supplier_menu_df</span> <span class="o">=</span>  <span class="n">get_electric_supplier_menu_data</span><span class="p">(</span><span class="n">excel_file</span><span class="p">,</span> <span class="n">sheet_name</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L137" class="lines-num"><span id="L137" data-line-number="137"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L137" class="lines-code chroma"><code class="code-inner">                        <span class="c1"># PostgreS登録</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L138" class="lines-num"><span id="L138" data-line-number="138"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L138" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_insert</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L139" class="lines-num"><span id="L139" data-line-number="139"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L139" class="lines-code chroma"><code class="code-inner">                            <span class="n">postgre_conn</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L140" class="lines-num"><span id="L140" data-line-number="140"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L140" class="lines-code chroma"><code class="code-inner">                            <span class="n">electric_supplier_menu_df</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L141" class="lines-num"><span id="L141" data-line-number="141"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L141" class="lines-code chroma"><code class="code-inner">                            <span class="n">constants</span><span class="o">.</span><span class="n">MECF_COLUMNS</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L142" class="lines-num"><span id="L142" data-line-number="142"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L142" class="lines-code chroma"><code class="code-inner">                            <span class="n">schema_middle</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MECF</span><span class="o">.</span><span class="n">value</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L143" class="lines-num"><span id="L143" data-line-number="143"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L143" class="lines-code chroma"><code class="code-inner">                        <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L144" class="lines-num"><span id="L144" data-line-number="144"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L144" class="lines-code chroma"><code class="code-inner">                        
</code></td>
						</tr>
						
						
						<tr>
							<td id="L145" class="lines-num"><span id="L145" data-line-number="145"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L145" class="lines-code chroma"><code class="code-inner">                        <span class="c1"># execute_update(conn, </span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L146" class="lines-num"><span id="L146" data-line-number="146"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L146" class="lines-code chroma"><code class="code-inner">                        <span class="c1">#                schema_middle + DOT + constants.MasterTable.MECF.value, </span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L147" class="lines-num"><span id="L147" data-line-number="147"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L147" class="lines-code chroma"><code class="code-inner">                        <span class="c1">#                {&#34;delete_flg&#34;:True},</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L148" class="lines-num"><span id="L148" data-line-number="148"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L148" class="lines-code chroma"><code class="code-inner">                        <span class="c1">#                {&#34;delete_flg&#34;:[False, None]})</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L149" class="lines-num"><span id="L149" data-line-number="149"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L149" class="lines-code chroma"><code class="code-inner">                        
</code></td>
						</tr>
						
						
						<tr>
							<td id="L150" class="lines-num"><span id="L150" data-line-number="150"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L150" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_hive_update</span><span class="p">(</span><span class="n">corp_conn</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L151" class="lines-num"><span id="L151" data-line-number="151"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L151" class="lines-code chroma"><code class="code-inner">                                            <span class="n">schema_middle</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MECF</span><span class="o">.</span><span class="n">value</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L152" class="lines-num"><span id="L152" data-line-number="152"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L152" class="lines-code chroma"><code class="code-inner">                                            <span class="n">constants</span><span class="o">.</span><span class="n">MECF_COLUMNS</span><span class="p">,</span> <span class="kc">False</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L153" class="lines-num"><span id="L153" data-line-number="153"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L153" class="lines-code chroma"><code class="code-inner">                        <span class="c1"># Hive登録</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L154" class="lines-num"><span id="L154" data-line-number="154"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L154" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_insert</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L155" class="lines-num"><span id="L155" data-line-number="155"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L155" class="lines-code chroma"><code class="code-inner">                            <span class="n">corp_conn</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L156" class="lines-num"><span id="L156" data-line-number="156"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L156" class="lines-code chroma"><code class="code-inner">                            <span class="n">electric_supplier_menu_df</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L157" class="lines-num"><span id="L157" data-line-number="157"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L157" class="lines-code chroma"><code class="code-inner">                            <span class="n">constants</span><span class="o">.</span><span class="n">MECF_COLUMNS</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L158" class="lines-num"><span id="L158" data-line-number="158"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L158" class="lines-code chroma"><code class="code-inner">                            <span class="n">schema_middle</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MECF</span><span class="o">.</span><span class="n">value</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L159" class="lines-num"><span id="L159" data-line-number="159"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L159" class="lines-code chroma"><code class="code-inner">                        <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L160" class="lines-num"><span id="L160" data-line-number="160"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L160" class="lines-code chroma"><code class="code-inner">                    <span class="k">if</span> <span class="ow">not</span> <span class="n">industry_sheet_flg</span> <span class="ow">and</span> <span class="n">sheet_name</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="n">constants</span><span class="o">.</span><span class="n">EEGSMasterSheetName</span><span class="o">.</span><span class="n">MJSIC_SHEET_NAME</span><span class="o">.</span><span class="n">value</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L161" class="lines-num"><span id="L161" data-line-number="161"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L161" class="lines-code chroma"><code class="code-inner">                        <span class="n">industry_sheet_flg</span> <span class="o">=</span> <span class="kc">True</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L162" class="lines-num"><span id="L162" data-line-number="162"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L162" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_delete</span><span class="p">(</span><span class="n">postgre_conn</span><span class="p">,</span> <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MJSIC</span><span class="o">.</span><span class="n">value</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L163" class="lines-num"><span id="L163" data-line-number="163"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L163" class="lines-code chroma"><code class="code-inner">                        <span class="n">industy_classification_df</span> <span class="o">=</span> <span class="n">get_industy_classification_mst</span><span class="p">(</span><span class="n">excel_file</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L164" class="lines-num"><span id="L164" data-line-number="164"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L164" class="lines-code chroma"><code class="code-inner">                        <span class="c1"># PostgreS登録</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L165" class="lines-num"><span id="L165" data-line-number="165"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L165" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_insert</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L166" class="lines-num"><span id="L166" data-line-number="166"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L166" class="lines-code chroma"><code class="code-inner">                            <span class="n">postgre_conn</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L167" class="lines-num"><span id="L167" data-line-number="167"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L167" class="lines-code chroma"><code class="code-inner">                            <span class="n">industy_classification_df</span><span class="p">,</span>  
</code></td>
						</tr>
						
						
						<tr>
							<td id="L168" class="lines-num"><span id="L168" data-line-number="168"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L168" class="lines-code chroma"><code class="code-inner">                            <span class="n">constants</span><span class="o">.</span><span class="n">MJSIC_COLUMNS</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L169" class="lines-num"><span id="L169" data-line-number="169"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L169" class="lines-code chroma"><code class="code-inner">                            <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MJSIC</span><span class="o">.</span><span class="n">value</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L170" class="lines-num"><span id="L170" data-line-number="170"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L170" class="lines-code chroma"><code class="code-inner">                        <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L171" class="lines-num"><span id="L171" data-line-number="171"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L171" class="lines-code chroma"><code class="code-inner">                        
</code></td>
						</tr>
						
						
						<tr>
							<td id="L172" class="lines-num"><span id="L172" data-line-number="172"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L172" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_hive_update</span><span class="p">(</span><span class="n">common_conn</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L173" class="lines-num"><span id="L173" data-line-number="173"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L173" class="lines-code chroma"><code class="code-inner">                                            <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MJSIC</span><span class="o">.</span><span class="n">value</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L174" class="lines-num"><span id="L174" data-line-number="174"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L174" class="lines-code chroma"><code class="code-inner">                                           <span class="n">constants</span><span class="o">.</span><span class="n">MJSIC_COLUMNS</span><span class="p">,</span> <span class="kc">False</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L175" class="lines-num"><span id="L175" data-line-number="175"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L175" class="lines-code chroma"><code class="code-inner">                        <span class="c1"># Hive登録</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L176" class="lines-num"><span id="L176" data-line-number="176"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L176" class="lines-code chroma"><code class="code-inner">                        <span class="n">execute_insert</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L177" class="lines-num"><span id="L177" data-line-number="177"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L177" class="lines-code chroma"><code class="code-inner">                            <span class="n">common_conn</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L178" class="lines-num"><span id="L178" data-line-number="178"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L178" class="lines-code chroma"><code class="code-inner">                            <span class="n">industy_classification_df</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L179" class="lines-num"><span id="L179" data-line-number="179"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L179" class="lines-code chroma"><code class="code-inner">                            <span class="n">constants</span><span class="o">.</span><span class="n">MJSIC_COLUMNS</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L180" class="lines-num"><span id="L180" data-line-number="180"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L180" class="lines-code chroma"><code class="code-inner">                            <span class="n">schema_commom</span> <span class="o">+</span> <span class="n">DOT</span> <span class="o">+</span> <span class="n">constants</span><span class="o">.</span><span class="n">MasterTable</span><span class="o">.</span><span class="n">MJSIC</span><span class="o">.</span><span class="n">value</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L181" class="lines-num"><span id="L181" data-line-number="181"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L181" class="lines-code chroma"><code class="code-inner">                        <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L182" class="lines-num"><span id="L182" data-line-number="182"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L182" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L183" class="lines-num"><span id="L183" data-line-number="183"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L183" class="lines-code chroma"><code class="code-inner">        <span class="k">except</span> <span class="n">DatabaseError</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L184" class="lines-num"><span id="L184" data-line-number="184"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L184" class="lines-code chroma"><code class="code-inner">            <span class="n">error_message</span> <span class="o">=</span> <span class="n">traceback</span><span class="o">.</span><span class="n">format_exc</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L185" class="lines-num"><span id="L185" data-line-number="185"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L185" class="lines-code chroma"><code class="code-inner">            <span class="n">error_line</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="n">e</span><span class="o">.</span><span class="n">__traceback__</span><span class="o">.</span><span class="n">tb_lineno</span><span class="p">)</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L186" class="lines-num"><span id="L186" data-line-number="186"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L186" class="lines-code chroma"><code class="code-inner">            <span class="n">logger</span><span class="o">.</span><span class="n">error</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;</span><span class="s2"> DatabaseError occurred at line </span><span class="si">{</span><span class="n">error_line</span><span class="si">}</span><span class="s2">: </span><span class="si">{</span><span class="n">error_message</span><span class="si">}</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L187" class="lines-num"><span id="L187" data-line-number="187"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L187" class="lines-code chroma"><code class="code-inner">            <span class="k">raise</span> <span class="n">e</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L188" class="lines-num"><span id="L188" data-line-number="188"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L188" class="lines-code chroma"><code class="code-inner">        
</code></td>
						</tr>
						
						
						<tr>
							<td id="L189" class="lines-num"><span id="L189" data-line-number="189"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L189" class="lines-code chroma"><code class="code-inner">        <span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L190" class="lines-num"><span id="L190" data-line-number="190"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L190" class="lines-code chroma"><code class="code-inner">            <span class="n">error_message</span> <span class="o">=</span> <span class="n">traceback</span><span class="o">.</span><span class="n">format_exc</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L191" class="lines-num"><span id="L191" data-line-number="191"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L191" class="lines-code chroma"><code class="code-inner">            <span class="n">error_line</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="n">e</span><span class="o">.</span><span class="n">__traceback__</span><span class="o">.</span><span class="n">tb_lineno</span><span class="p">)</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L192" class="lines-num"><span id="L192" data-line-number="192"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L192" class="lines-code chroma"><code class="code-inner">            <span class="n">logger</span><span class="o">.</span><span class="n">error</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;</span><span class="s2"> Error occurred at line </span><span class="si">{</span><span class="n">error_line</span><span class="si">}</span><span class="s2">: </span><span class="si">{</span><span class="n">error_message</span><span class="si">}</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L193" class="lines-num"><span id="L193" data-line-number="193"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L193" class="lines-code chroma"><code class="code-inner">            <span class="k">raise</span> <span class="n">e</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L194" class="lines-num"><span id="L194" data-line-number="194"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L194" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L195" class="lines-num"><span id="L195" data-line-number="195"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L195" class="lines-code chroma"><code class="code-inner">        <span class="k">finally</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L196" class="lines-num"><span id="L196" data-line-number="196"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L196" class="lines-code chroma"><code class="code-inner">            <span class="c1"># リソースのクリーンアップ</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L197" class="lines-num"><span id="L197" data-line-number="197"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L197" class="lines-code chroma"><code class="code-inner">            <span class="c1"># connectionをクローズする</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L198" class="lines-num"><span id="L198" data-line-number="198"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L198" class="lines-code chroma"><code class="code-inner">            <span class="k">if</span> <span class="n">hive_common_connect_singleton</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L199" class="lines-num"><span id="L199" data-line-number="199"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L199" class="lines-code chroma"><code class="code-inner">                <span class="n">hive_common_connect_singleton</span><span class="o">.</span><span class="n">close_connection</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L200" class="lines-num"><span id="L200" data-line-number="200"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L200" class="lines-code chroma"><code class="code-inner">            <span class="k">if</span> <span class="n">hive_corp_connect_singleton</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L201" class="lines-num"><span id="L201" data-line-number="201"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L201" class="lines-code chroma"><code class="code-inner">                <span class="n">hive_corp_connect_singleton</span><span class="o">.</span><span class="n">close_connection</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L202" class="lines-num"><span id="L202" data-line-number="202"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L202" class="lines-code chroma"><code class="code-inner">            <span class="k">if</span> <span class="n">postgre_connect_singleton</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L203" class="lines-num"><span id="L203" data-line-number="203"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L203" class="lines-code chroma"><code class="code-inner">                <span class="n">postgre_connect_singleton</span><span class="o">.</span><span class="n">close_connection</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L204" class="lines-num"><span id="L204" data-line-number="204"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L204" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L205" class="lines-num"><span id="L205" data-line-number="205"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L205" class="lines-code chroma"><code class="code-inner"><span class="k">def</span> <span class="nf">extract_supplier_name</span><span class="p">(</span><span class="n">menu_name</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L206" class="lines-num"><span id="L206" data-line-number="206"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L206" class="lines-code chroma"><code class="code-inner">    <span class="sa"></span><span class="s2">&#34;&#34;&#34;</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L207" class="lines-num"><span id="L207" data-line-number="207"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L207" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    メニュー名称から電気事業者名を抽出する。</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L208" class="lines-num"><span id="L208" data-line-number="208"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L208" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    「（株）」の後ろにメニューがある場合、それを削除する。</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L209" class="lines-num"><span id="L209" data-line-number="209"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L209" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    </span><span class="s2">&#34;&#34;&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L210" class="lines-num"><span id="L210" data-line-number="210"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L210" class="lines-code chroma"><code class="code-inner">    <span class="k">match</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="sa">r</span><span class="s2">&#34;</span><span class="s2">^((?:（株）|</span><span class="s2">\</span><span class="s2">(株</span><span class="s2">\</span><span class="s2">)|[^</span><span class="s2">\</span><span class="s2">(</span><span class="s2">\</span><span class="s2">)（）]+)+)</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">menu_name</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L211" class="lines-num"><span id="L211" data-line-number="211"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L211" class="lines-code chroma"><code class="code-inner">    <span class="k">if</span> <span class="k">match</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L212" class="lines-num"><span id="L212" data-line-number="212"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L212" class="lines-code chroma"><code class="code-inner">        <span class="n">supplier_name</span> <span class="o">=</span> <span class="k">match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span><span class="o">.</span><span class="n">strip</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L213" class="lines-num"><span id="L213" data-line-number="213"></span></td>
							
								<td class="lines-escape"><button class="toggle-escape-button btn interact-bg" title="この行には不可視のUnicode文字があります "></button></td>
							
							<td rel="L213" class="lines-code chroma"><code class="code-inner">        <span class="k">return</span> <span class="n">re</span><span class="o">.</span><span class="n">sub</span><span class="p">(</span><span class="sa">r</span><span class="s2">&#34;</span><span class="s2">[ <span class="escaped-code-point" data-escaped="[U+3000]"><span class="char">　</span></span>]*メニュー.*$</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">supplier_name</span><span class="p">)</span>  <span class="c1"># 「メニュー〇〇」を削除</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L214" class="lines-num"><span id="L214" data-line-number="214"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L214" class="lines-code chroma"><code class="code-inner">    <span class="k">return</span> <span class="n">menu_name</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L215" class="lines-num"><span id="L215" data-line-number="215"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L215" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L216" class="lines-num"><span id="L216" data-line-number="216"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L216" class="lines-code chroma"><code class="code-inner"><span class="k">def</span> <span class="nf">set_system_column</span><span class="p">(</span><span class="n">result_df</span><span class="p">,</span> <span class="n">schema_name</span><span class="o">=</span><span class="kc">None</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L217" class="lines-num"><span id="L217" data-line-number="217"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L217" class="lines-code chroma"><code class="code-inner">    <span class="sa"></span><span class="s2">&#34;&#34;&#34;</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L218" class="lines-num"><span id="L218" data-line-number="218"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L218" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    システムカラム情報設定</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L219" class="lines-num"><span id="L219" data-line-number="219"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L219" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    </span><span class="s2">&#34;&#34;&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L220" class="lines-num"><span id="L220" data-line-number="220"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L220" class="lines-code chroma"><code class="code-inner">     <span class="c1"># excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L221" class="lines-num"><span id="L221" data-line-number="221"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L221" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">START_DATE</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="sa"></span><span class="s1">&#39;</span><span class="s1">20240401</span><span class="s1">&#39;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L222" class="lines-num"><span id="L222" data-line-number="222"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L222" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">END_DATE</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L223" class="lines-num"><span id="L223" data-line-number="223"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L223" class="lines-code chroma"><code class="code-inner">    <span class="k">if</span> <span class="n">schema_name</span> <span class="ow">is</span> <span class="ow">not</span> <span class="kc">None</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L224" class="lines-num"><span id="L224" data-line-number="224"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L224" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">CREATION_DATETIME</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;</span><span class="si">{</span><span class="n">current_timestamp</span><span class="si">}</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L225" class="lines-num"><span id="L225" data-line-number="225"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L225" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">CREATE_BY</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;</span><span class="si">{</span><span class="n">creator_name</span><span class="si">}</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L226" class="lines-num"><span id="L226" data-line-number="226"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L226" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">UPDATE_DATETIME</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L227" class="lines-num"><span id="L227" data-line-number="227"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L227" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">UPDATE_BY</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L228" class="lines-num"><span id="L228" data-line-number="228"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L228" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">DELETE_FLG</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L229" class="lines-num"><span id="L229" data-line-number="229"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L229" class="lines-code chroma"><code class="code-inner">    <span class="k">else</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L230" class="lines-num"><span id="L230" data-line-number="230"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L230" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">CREATED_AT</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;</span><span class="si">{</span><span class="n">current_timestamp</span><span class="si">}</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L231" class="lines-num"><span id="L231" data-line-number="231"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L231" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">CREATED_BY</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;</span><span class="si">{</span><span class="n">creator_name</span><span class="si">}</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L232" class="lines-num"><span id="L232" data-line-number="232"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L232" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">UPDATED_AT</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L233" class="lines-num"><span id="L233" data-line-number="233"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L233" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">UPDATED_BY</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L234" class="lines-num"><span id="L234" data-line-number="234"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L234" class="lines-code chroma"><code class="code-inner">        <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">DELETE_FLAG</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L235" class="lines-num"><span id="L235" data-line-number="235"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L235" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L236" class="lines-num"><span id="L236" data-line-number="236"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L236" class="lines-code chroma"><code class="code-inner"><span class="k">def</span> <span class="nf">get_electric_supplier_menu_data</span><span class="p">(</span><span class="n">excel_file</span><span class="p">,</span> <span class="n">sheet_name</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L237" class="lines-num"><span id="L237" data-line-number="237"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L237" class="lines-code chroma"><code class="code-inner">    <span class="sa"></span><span class="s2">&#34;&#34;&#34;</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L238" class="lines-num"><span id="L238" data-line-number="238"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L238" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    電力会社の排出係数マスタデータ取得</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L239" class="lines-num"><span id="L239" data-line-number="239"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L239" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    </span><span class="s2">&#34;&#34;&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L240" class="lines-num"><span id="L240" data-line-number="240"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L240" class="lines-code chroma"><code class="code-inner">    <span class="c1"># Excelファイルを読み込む</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L241" class="lines-num"><span id="L241" data-line-number="241"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L241" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_excel</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L242" class="lines-num"><span id="L242" data-line-number="242"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L242" class="lines-code chroma"><code class="code-inner">        <span class="n">excel_file</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L243" class="lines-num"><span id="L243" data-line-number="243"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L243" class="lines-code chroma"><code class="code-inner">        <span class="n">sheet_name</span><span class="o">=</span> <span class="n">sheet_name</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L244" class="lines-num"><span id="L244" data-line-number="244"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L244" class="lines-code chroma"><code class="code-inner">        <span class="n">skiprows</span><span class="o">=</span><span class="mi">2</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L245" class="lines-num"><span id="L245" data-line-number="245"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L245" class="lines-code chroma"><code class="code-inner">    <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L246" class="lines-num"><span id="L246" data-line-number="246"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L246" class="lines-code chroma"><code class="code-inner">    
</code></td>
						</tr>
						
						
						<tr>
							<td id="L247" class="lines-num"><span id="L247" data-line-number="247"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L247" class="lines-code chroma"><code class="code-inner">    <span class="c1"># nanを空文字に変換</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L248" class="lines-num"><span id="L248" data-line-number="248"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L248" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span><span class="o">.</span><span class="n">fillna</span><span class="p">(</span><span class="n">BLANK</span><span class="p">,</span> <span class="n">inplace</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L249" class="lines-num"><span id="L249" data-line-number="249"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L249" class="lines-code chroma"><code class="code-inner">    <span class="c1"># &#39;-&#39;を空文字に変換</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L250" class="lines-num"><span id="L250" data-line-number="250"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L250" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="n">HYPHEN</span><span class="p">,</span> <span class="n">BLANK</span><span class="p">,</span> <span class="n">inplace</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L251" class="lines-num"><span id="L251" data-line-number="251"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L251" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L252" class="lines-num"><span id="L252" data-line-number="252"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L252" class="lines-code chroma"><code class="code-inner">    <span class="c1"># カラム名を設定</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L253" class="lines-num"><span id="L253" data-line-number="253"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L253" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span><span class="o">.</span><span class="n">columns</span> <span class="o">=</span> <span class="p">[</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L254" class="lines-num"><span id="L254" data-line-number="254"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L254" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気事業者登録番号</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">公表回数</span><span class="s2">&#34;</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L255" class="lines-num"><span id="L255" data-line-number="255"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L255" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー番号</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">調整後排出係数</span><span class="s2">&#34;</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L256" class="lines-num"><span id="L256" data-line-number="256"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L256" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">非化石証書の使用状況</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">基礎排出係数</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L257" class="lines-num"><span id="L257" data-line-number="257"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L257" class="lines-code chroma"><code class="code-inner">    <span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L258" class="lines-num"><span id="L258" data-line-number="258"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L258" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L259" class="lines-num"><span id="L259" data-line-number="259"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L259" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 余計なスペースを削除</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L260" class="lines-num"><span id="L260" data-line-number="260"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L260" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">applymap</span><span class="p">(</span><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="n">x</span><span class="o">.</span><span class="n">strip</span><span class="p">(</span><span class="p">)</span> <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">else</span> <span class="n">x</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L261" class="lines-num"><span id="L261" data-line-number="261"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L261" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L262" class="lines-num"><span id="L262" data-line-number="262"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L262" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 削除フラグが 0 のデータのみ対象</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L263" class="lines-num"><span id="L263" data-line-number="263"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L263" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="n">df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L264" class="lines-num"><span id="L264" data-line-number="264"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L264" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L265" class="lines-num"><span id="L265" data-line-number="265"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L265" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 「【使用不可】」を含む行を除外</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L266" class="lines-num"><span id="L266" data-line-number="266"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L266" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="o">~</span><span class="n">df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span><span class="o">.</span><span class="n">str</span><span class="o">.</span><span class="n">contains</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">【使用不可】</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">regex</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">na</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L267" class="lines-num"><span id="L267" data-line-number="267"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L267" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L268" class="lines-num"><span id="L268" data-line-number="268"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L268" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 各電気事業者ごとに報告年度ごとの最大公表回数を取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L269" class="lines-num"><span id="L269" data-line-number="269"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L269" class="lines-code chroma"><code class="code-inner">    <span class="n">max_reports_per_year</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">groupby</span><span class="p">(</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気事業者登録番号</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">公表回数</span><span class="s2">&#34;</span><span class="p">]</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="p">)</span><span class="o">.</span><span class="n">reset_index</span><span class="p">(</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L270" class="lines-num"><span id="L270" data-line-number="270"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L270" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L271" class="lines-num"><span id="L271" data-line-number="271"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L271" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 最大公表回数に一致するデータのみ抽出</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L272" class="lines-num"><span id="L272" data-line-number="272"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L272" class="lines-code chroma"><code class="code-inner">    <span class="n">df_latest</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">merge</span><span class="p">(</span><span class="n">max_reports_per_year</span><span class="p">,</span> <span class="n">on</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気事業者登録番号</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">公表回数</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L273" class="lines-num"><span id="L273" data-line-number="273"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L273" class="lines-code chroma"><code class="code-inner">    
</code></td>
						</tr>
						
						
						<tr>
							<td id="L274" class="lines-num"><span id="L274" data-line-number="274"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L274" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 結果を格納する辞書を用意</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L275" class="lines-num"><span id="L275" data-line-number="275"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L275" class="lines-code chroma"><code class="code-inner">    <span class="n">selected_coefficients</span> <span class="o">=</span> <span class="p">{</span><span class="p">}</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L276" class="lines-num"><span id="L276" data-line-number="276"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L276" class="lines-code chroma"><code class="code-inner">    <span class="n">menu_names</span> <span class="o">=</span> <span class="p">{</span><span class="p">}</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L277" class="lines-num"><span id="L277" data-line-number="277"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L277" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L278" class="lines-num"><span id="L278" data-line-number="278"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L278" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 電気事業者登録番号ごとに処理</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L279" class="lines-num"><span id="L279" data-line-number="279"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L279" class="lines-code chroma"><code class="code-inner">    <span class="k">for</span> <span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">,</span> <span class="n">group</span> <span class="ow">in</span> <span class="n">df_latest</span><span class="o">.</span><span class="n">groupby</span><span class="p">(</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気事業者登録番号</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L280" class="lines-num"><span id="L280" data-line-number="280"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L280" class="lines-code chroma"><code class="code-inner">        <span class="c1"># 「（残差）」を含む行を取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L281" class="lines-num"><span id="L281" data-line-number="281"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L281" class="lines-code chroma"><code class="code-inner">        <span class="n">residual_row</span> <span class="o">=</span> <span class="n">group</span><span class="p">[</span><span class="n">group</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span><span class="o">.</span><span class="n">str</span><span class="o">.</span><span class="n">contains</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">残差</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">regex</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">na</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L282" class="lines-num"><span id="L282" data-line-number="282"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L282" class="lines-code chroma"><code class="code-inner">        
</code></td>
						</tr>
						
						
						<tr>
							<td id="L283" class="lines-num"><span id="L283" data-line-number="283"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L283" class="lines-code chroma"><code class="code-inner">        <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">group</span><span class="p">)</span> <span class="o">==</span> <span class="mi">1</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L284" class="lines-num"><span id="L284" data-line-number="284"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L284" class="lines-code chroma"><code class="code-inner">            <span class="c1"># 1つのデータしかない場合</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L285" class="lines-num"><span id="L285" data-line-number="285"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L285" class="lines-code chroma"><code class="code-inner">            <span class="n">selected_coefficients</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">group</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">調整後排出係数</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L286" class="lines-num"><span id="L286" data-line-number="286"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L286" class="lines-code chroma"><code class="code-inner">            <span class="n">menu_names</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">group</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L287" class="lines-num"><span id="L287" data-line-number="287"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L287" class="lines-code chroma"><code class="code-inner">        <span class="k">elif</span> <span class="ow">not</span> <span class="n">residual_row</span><span class="o">.</span><span class="n">empty</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L288" class="lines-num"><span id="L288" data-line-number="288"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L288" class="lines-code chroma"><code class="code-inner">            <span class="c1"># 「残差」がある場合</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L289" class="lines-num"><span id="L289" data-line-number="289"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L289" class="lines-code chroma"><code class="code-inner">            <span class="n">selected_coefficients</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">residual_row</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">調整後排出係数</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L290" class="lines-num"><span id="L290" data-line-number="290"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L290" class="lines-code chroma"><code class="code-inner">            <span class="n">menu_names</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">residual_row</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L291" class="lines-num"><span id="L291" data-line-number="291"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L291" class="lines-code chroma"><code class="code-inner">        <span class="k">else</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L292" class="lines-num"><span id="L292" data-line-number="292"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L292" class="lines-code chroma"><code class="code-inner">            <span class="c1"># 「（参考値）」を含む行を取得</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L293" class="lines-num"><span id="L293" data-line-number="293"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L293" class="lines-code chroma"><code class="code-inner">            <span class="n">reference_row</span> <span class="o">=</span> <span class="n">group</span><span class="p">[</span><span class="n">group</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span><span class="o">.</span><span class="n">str</span><span class="o">.</span><span class="n">contains</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">参考値</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">regex</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">na</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L294" class="lines-num"><span id="L294" data-line-number="294"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L294" class="lines-code chroma"><code class="code-inner">            <span class="k">if</span> <span class="ow">not</span> <span class="n">reference_row</span><span class="o">.</span><span class="n">empty</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L295" class="lines-num"><span id="L295" data-line-number="295"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L295" class="lines-code chroma"><code class="code-inner">                <span class="n">selected_coefficients</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">reference_row</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">調整後排出係数</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L296" class="lines-num"><span id="L296" data-line-number="296"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L296" class="lines-code chroma"><code class="code-inner">                <span class="n">menu_names</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">reference_row</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L297" class="lines-num"><span id="L297" data-line-number="297"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L297" class="lines-code chroma"><code class="code-inner">            <span class="k">else</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L298" class="lines-num"><span id="L298" data-line-number="298"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L298" class="lines-code chroma"><code class="code-inner">                <span class="c1"># どれも該当しない場合は最初のデータを採用</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L299" class="lines-num"><span id="L299" data-line-number="299"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L299" class="lines-code chroma"><code class="code-inner">                <span class="n">selected_coefficients</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">group</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">調整後排出係数</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L300" class="lines-num"><span id="L300" data-line-number="300"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L300" class="lines-code chroma"><code class="code-inner">                <span class="n">menu_names</span><span class="p">[</span><span class="p">(</span><span class="n">business_id</span><span class="p">,</span> <span class="n">report_year</span><span class="p">)</span><span class="p">]</span> <span class="o">=</span> <span class="n">group</span><span class="o">.</span><span class="n">iloc</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L301" class="lines-num"><span id="L301" data-line-number="301"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L301" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L302" class="lines-num"><span id="L302" data-line-number="302"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L302" class="lines-code chroma"><code class="code-inner">    <span class="c1"># タプルキーを展開して DataFrame を作成</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L303" class="lines-num"><span id="L303" data-line-number="303"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L303" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L304" class="lines-num"><span id="L304" data-line-number="304"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L304" class="lines-code chroma"><code class="code-inner">        <span class="p">[</span><span class="p">(</span><span class="n">key</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="p">,</span> <span class="n">key</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="p">,</span> <span class="n">value</span><span class="p">)</span> <span class="k">for</span> <span class="n">key</span><span class="p">,</span> <span class="n">value</span> <span class="ow">in</span> <span class="n">selected_coefficients</span><span class="o">.</span><span class="n">items</span><span class="p">(</span><span class="p">)</span><span class="p">]</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L305" class="lines-num"><span id="L305" data-line-number="305"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L305" class="lines-code chroma"><code class="code-inner">        <span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気事業者登録番号</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">調整後排出係数</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L306" class="lines-num"><span id="L306" data-line-number="306"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L306" class="lines-code chroma"><code class="code-inner">    <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L307" class="lines-num"><span id="L307" data-line-number="307"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L307" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L308" class="lines-num"><span id="L308" data-line-number="308"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L308" class="lines-code chroma"><code class="code-inner">    <span class="c1"># メニュー名称を追加</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L309" class="lines-num"><span id="L309" data-line-number="309"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L309" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="n">result_df</span><span class="o">.</span><span class="n">set_index</span><span class="p">(</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気事業者登録番号</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span><span class="o">.</span><span class="n">index</span><span class="o">.</span><span class="n">map</span><span class="p">(</span><span class="n">menu_names</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L310" class="lines-num"><span id="L310" data-line-number="310"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L310" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L311" class="lines-num"><span id="L311" data-line-number="311"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L311" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 電気事業者名を取得（extract_supplier_name() 関数が必要）</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L312" class="lines-num"><span id="L312" data-line-number="312"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L312" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">=</span> <span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">]</span><span class="o">.</span><span class="n">apply</span><span class="p">(</span><span class="n">extract_supplier_name</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L313" class="lines-num"><span id="L313" data-line-number="313"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L313" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L314" class="lines-num"><span id="L314" data-line-number="314"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L314" class="lines-code chroma"><code class="code-inner">    <span class="c1"># カラム名を英字に変換</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L315" class="lines-num"><span id="L315" data-line-number="315"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L315" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span> <span class="o">=</span> <span class="n">result_df</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">{</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L316" class="lines-num"><span id="L316" data-line-number="316"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L316" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気事業者登録番号</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">REGISTRATION_NUMBER</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L317" class="lines-num"><span id="L317" data-line-number="317"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L317" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">メニュー名称</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ELECTRICITY_SUPPLIER_NAME</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L318" class="lines-num"><span id="L318" data-line-number="318"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L318" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">FISCAL_YEAR</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L319" class="lines-num"><span id="L319" data-line-number="319"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L319" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">調整後排出係数</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ADJUSTED_EMISSION_FACTOR</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L320" class="lines-num"><span id="L320" data-line-number="320"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L320" class="lines-code chroma"><code class="code-inner">    <span class="p">}</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L321" class="lines-num"><span id="L321" data-line-number="321"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L321" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L322" class="lines-num"><span id="L322" data-line-number="322"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L322" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 出力順番を指定</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L323" class="lines-num"><span id="L323" data-line-number="323"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L323" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span> <span class="o">=</span> <span class="n">result_df</span><span class="p">[</span><span class="p">[</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L324" class="lines-num"><span id="L324" data-line-number="324"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L324" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">REGISTRATION_NUMBER</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L325" class="lines-num"><span id="L325" data-line-number="325"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L325" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ELECTRICITY_SUPPLIER_NAME</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L326" class="lines-num"><span id="L326" data-line-number="326"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L326" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">FISCAL_YEAR</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L327" class="lines-num"><span id="L327" data-line-number="327"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L327" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ADJUSTED_EMISSION_FACTOR</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L328" class="lines-num"><span id="L328" data-line-number="328"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L328" class="lines-code chroma"><code class="code-inner">    <span class="p">]</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L329" class="lines-num"><span id="L329" data-line-number="329"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L329" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L330" class="lines-num"><span id="L330" data-line-number="330"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L330" class="lines-code chroma"><code class="code-inner">    <span class="c1"># excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L331" class="lines-num"><span id="L331" data-line-number="331"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L331" class="lines-code chroma"><code class="code-inner">    <span class="n">set_system_column</span><span class="p">(</span><span class="n">result_df</span><span class="p">,</span> <span class="n">schema_middle</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L332" class="lines-num"><span id="L332" data-line-number="332"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L332" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L333" class="lines-num"><span id="L333" data-line-number="333"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L333" class="lines-code chroma"><code class="code-inner">    <span class="c1"># CSVに出力</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L334" class="lines-num"><span id="L334" data-line-number="334"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L334" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span><span class="o">.</span><span class="n">to_csv</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">electric_supplier_menu.csv</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">index</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L335" class="lines-num"><span id="L335" data-line-number="335"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L335" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L336" class="lines-num"><span id="L336" data-line-number="336"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L336" class="lines-code chroma"><code class="code-inner">    <span class="k">return</span> <span class="n">result_df</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L337" class="lines-num"><span id="L337" data-line-number="337"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L337" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L338" class="lines-num"><span id="L338" data-line-number="338"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L338" class="lines-code chroma"><code class="code-inner"><span class="k">def</span> <span class="nf">get_activity_minor_category_data</span><span class="p">(</span><span class="n">excel_file</span><span class="p">,</span> <span class="n">sheet_name</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L339" class="lines-num"><span id="L339" data-line-number="339"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L339" class="lines-code chroma"><code class="code-inner">    <span class="sa"></span><span class="s2">&#34;&#34;&#34;</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L340" class="lines-num"><span id="L340" data-line-number="340"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L340" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    活動項目小分類（事業者）マスタデータ取得</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L341" class="lines-num"><span id="L341" data-line-number="341"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L341" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    </span><span class="s2">&#34;&#34;&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L342" class="lines-num"><span id="L342" data-line-number="342"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L342" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L343" class="lines-num"><span id="L343" data-line-number="343"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L343" class="lines-code chroma"><code class="code-inner">    <span class="c1"># Excelファイルを読み込む</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L344" class="lines-num"><span id="L344" data-line-number="344"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L344" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_excel</span><span class="p">(</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L345" class="lines-num"><span id="L345" data-line-number="345"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L345" class="lines-code chroma"><code class="code-inner">        <span class="n">excel_file</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L346" class="lines-num"><span id="L346" data-line-number="346"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L346" class="lines-code chroma"><code class="code-inner">        <span class="n">sheet_name</span><span class="o">=</span> <span class="n">sheet_name</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L347" class="lines-num"><span id="L347" data-line-number="347"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L347" class="lines-code chroma"><code class="code-inner">        <span class="n">skiprows</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L348" class="lines-num"><span id="L348" data-line-number="348"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L348" class="lines-code chroma"><code class="code-inner">        <span class="n">dtype</span><span class="o">=</span><span class="p">{</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目大分類ID</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L349" class="lines-num"><span id="L349" data-line-number="349"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L349" class="lines-code chroma"><code class="code-inner">               <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目中分類ID</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L350" class="lines-num"><span id="L350" data-line-number="350"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L350" class="lines-code chroma"><code class="code-inner">               <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目小分類ID</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L351" class="lines-num"><span id="L351" data-line-number="351"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L351" class="lines-code chroma"><code class="code-inner">               <span class="sa"></span><span class="s2">&#34;</span><span class="s2">表示順</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L352" class="lines-num"><span id="L352" data-line-number="352"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L352" class="lines-code chroma"><code class="code-inner">                <span class="sa"></span><span class="s2">&#34;</span><span class="s2">補助画面表示区分</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">Int64</span><span class="s2">&#34;</span><span class="p">,</span> <span class="p">}</span> <span class="c1"># 99.0になってしまうため</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L353" class="lines-num"><span id="L353" data-line-number="353"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L353" class="lines-code chroma"><code class="code-inner">    <span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L354" class="lines-num"><span id="L354" data-line-number="354"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L354" class="lines-code chroma"><code class="code-inner">    <span class="n">columns_to_fix</span> <span class="o">=</span> <span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（CH4）</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（N2O）</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（HFC）</span><span class="s2">&#34;</span><span class="p">,</span> 
</code></td>
						</tr>
						
						
						<tr>
							<td id="L355" class="lines-num"><span id="L355" data-line-number="355"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L355" class="lines-code chroma"><code class="code-inner">                  <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（PFC）</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（SF6）</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（NF3）</span><span class="s2">&#34;</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L356" class="lines-num"><span id="L356" data-line-number="356"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L356" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 指数表記防ぐため</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L357" class="lines-num"><span id="L357" data-line-number="357"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L357" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span><span class="p">[</span><span class="n">columns_to_fix</span><span class="p">]</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="n">columns_to_fix</span><span class="p">]</span><span class="o">.</span><span class="n">applymap</span><span class="p">(</span><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="sa">f</span><span class="s2">&#34;</span><span class="si">{</span><span class="n">x</span><span class="si">:</span><span class="s2">.10f</span><span class="si">}</span><span class="s2">&#34;</span> <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="nb">float</span><span class="p">)</span> <span class="k">else</span> <span class="n">x</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L358" class="lines-num"><span id="L358" data-line-number="358"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L358" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L359" class="lines-num"><span id="L359" data-line-number="359"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L359" class="lines-code chroma"><code class="code-inner">    <span class="c1"># nanを空文字に変換</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L360" class="lines-num"><span id="L360" data-line-number="360"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L360" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span><span class="o">.</span><span class="n">fillna</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">nan</span><span class="p">,</span> <span class="n">inplace</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L361" class="lines-num"><span id="L361" data-line-number="361"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L361" class="lines-code chroma"><code class="code-inner">    <span class="c1"># &#39;-&#39;を空文字に変換</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L362" class="lines-num"><span id="L362" data-line-number="362"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L362" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="n">HYPHEN</span><span class="p">,</span> <span class="n">BLANK</span><span class="p">,</span> <span class="n">inplace</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L363" class="lines-num"><span id="L363" data-line-number="363"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L363" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span><span class="p">:</span><span class="p">,</span> <span class="o">~</span><span class="n">df</span><span class="o">.</span><span class="n">columns</span><span class="o">.</span><span class="n">str</span><span class="o">.</span><span class="n">contains</span><span class="p">(</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">^Unnamed</span><span class="s2">&#34;</span><span class="p">)</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L364" class="lines-num"><span id="L364" data-line-number="364"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L364" class="lines-code chroma"><code class="code-inner">    <span class="c1"># カラム名を設定</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L365" class="lines-num"><span id="L365" data-line-number="365"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L365" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span><span class="o">.</span><span class="n">columns</span> <span class="o">=</span> <span class="p">[</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L366" class="lines-num"><span id="L366" data-line-number="366"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L366" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L367" class="lines-num"><span id="L367" data-line-number="367"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L367" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目大分類ID</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L368" class="lines-num"><span id="L368" data-line-number="368"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L368" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目中分類ID</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L369" class="lines-num"><span id="L369" data-line-number="369"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L369" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目小分類ID</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L370" class="lines-num"><span id="L370" data-line-number="370"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L370" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目小分類名</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L371" class="lines-num"><span id="L371" data-line-number="371"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L371" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">単位</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L372" class="lines-num"><span id="L372" data-line-number="372"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L372" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">換算係数</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L373" class="lines-num"><span id="L373" data-line-number="373"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L373" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">非化石エネルギー転換換算係数</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L374" class="lines-num"><span id="L374" data-line-number="374"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L374" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">非化石重み付け係数</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L375" class="lines-num"><span id="L375" data-line-number="375"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L375" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気需要最適化換算係数</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L376" class="lines-num"><span id="L376" data-line-number="376"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L376" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（エネ起CO2）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L377" class="lines-num"><span id="L377" data-line-number="377"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L377" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（非エネ起CO2）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L378" class="lines-num"><span id="L378" data-line-number="378"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L378" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（CH4）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L379" class="lines-num"><span id="L379" data-line-number="379"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L379" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（N2O）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L380" class="lines-num"><span id="L380" data-line-number="380"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L380" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（HFC）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L381" class="lines-num"><span id="L381" data-line-number="381"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L381" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（PFC）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L382" class="lines-num"><span id="L382" data-line-number="382"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L382" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（SF6）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L383" class="lines-num"><span id="L383" data-line-number="383"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L383" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（NF3）</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L384" class="lines-num"><span id="L384" data-line-number="384"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L384" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">変換値１</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L385" class="lines-num"><span id="L385" data-line-number="385"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L385" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">変換値２</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L386" class="lines-num"><span id="L386" data-line-number="386"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L386" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">非エネルギー区分</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L387" class="lines-num"><span id="L387" data-line-number="387"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L387" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">温対法フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L388" class="lines-num"><span id="L388" data-line-number="388"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L388" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">省エネ法フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L389" class="lines-num"><span id="L389" data-line-number="389"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L389" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目選択画面表示フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L390" class="lines-num"><span id="L390" data-line-number="390"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L390" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">補助画面表示区分</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L391" class="lines-num"><span id="L391" data-line-number="391"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L391" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">単位入力可否フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L392" class="lines-num"><span id="L392" data-line-number="392"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L392" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">換算係数入力可否フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L393" class="lines-num"><span id="L393" data-line-number="393"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L393" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">使用量入力可否フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L394" class="lines-num"><span id="L394" data-line-number="394"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L394" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">販売副生入力可否フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L395" class="lines-num"><span id="L395" data-line-number="395"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L395" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">購入未利用熱入力可否フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L396" class="lines-num"><span id="L396" data-line-number="396"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L396" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動量最大値</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L397" class="lines-num"><span id="L397" data-line-number="397"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L397" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動量最小値</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L398" class="lines-num"><span id="L398" data-line-number="398"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L398" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目コメント</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L399" class="lines-num"><span id="L399" data-line-number="399"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L399" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">熱関係補助画面表示フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L400" class="lines-num"><span id="L400" data-line-number="400"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L400" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気関係補助画面表示フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L401" class="lines-num"><span id="L401" data-line-number="401"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L401" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">化石・非化石区分</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L402" class="lines-num"><span id="L402" data-line-number="402"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L402" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">自家発電（他事業所からの供給）画面表示フラグ</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L403" class="lines-num"><span id="L403" data-line-number="403"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L403" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">表示順</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L404" class="lines-num"><span id="L404" data-line-number="404"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L404" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L405" class="lines-num"><span id="L405" data-line-number="405"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L405" class="lines-code chroma"><code class="code-inner">    <span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L406" class="lines-num"><span id="L406" data-line-number="406"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L406" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L407" class="lines-num"><span id="L407" data-line-number="407"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L407" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 余計なスペースを削除</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L408" class="lines-num"><span id="L408" data-line-number="408"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L408" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">applymap</span><span class="p">(</span><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="n">x</span><span class="o">.</span><span class="n">strip</span><span class="p">(</span><span class="p">)</span> <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">else</span> <span class="n">x</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L409" class="lines-num"><span id="L409" data-line-number="409"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L409" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L410" class="lines-num"><span id="L410" data-line-number="410"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L410" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 削除フラグが 0 のデータのみ対象</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L411" class="lines-num"><span id="L411" data-line-number="411"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L411" class="lines-code chroma"><code class="code-inner">    <span class="n">df</span> <span class="o">=</span> <span class="n">df</span><span class="p">[</span><span class="n">df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L412" class="lines-num"><span id="L412" data-line-number="412"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L412" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L413" class="lines-num"><span id="L413" data-line-number="413"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L413" class="lines-code chroma"><code class="code-inner">    <span class="c1"># カラム名を英字に変換</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L414" class="lines-num"><span id="L414" data-line-number="414"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L414" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span> <span class="o">=</span> <span class="n">df</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">{</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L415" class="lines-num"><span id="L415" data-line-number="415"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L415" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">報告年度</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">REPORT_YEAR</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L416" class="lines-num"><span id="L416" data-line-number="416"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L416" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目大分類ID</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MAJOR_CATEGORY_ID</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L417" class="lines-num"><span id="L417" data-line-number="417"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L417" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目中分類ID</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MIDDLE_CATEGORY_ID</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L418" class="lines-num"><span id="L418" data-line-number="418"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L418" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目小分類ID</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MINOR_CATEGORY_ID</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L419" class="lines-num"><span id="L419" data-line-number="419"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L419" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目小分類名</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MINOR_CATEGORY_NM</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L420" class="lines-num"><span id="L420" data-line-number="420"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L420" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">単位</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">UNIT</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L421" class="lines-num"><span id="L421" data-line-number="421"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L421" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">換算係数</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">CONVERSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L422" class="lines-num"><span id="L422" data-line-number="422"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L422" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">非化石エネルギー転換換算係数</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">NON_FOSSIL_CONV_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L423" class="lines-num"><span id="L423" data-line-number="423"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L423" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">非化石重み付け係数</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">NON_FOSSIL_WEIGHT_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L424" class="lines-num"><span id="L424" data-line-number="424"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L424" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気需要最適化換算係数</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ELECTRIC_DEMAND_OPT_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L425" class="lines-num"><span id="L425" data-line-number="425"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L425" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（エネ起CO2）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ENERGY_CO2_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L426" class="lines-num"><span id="L426" data-line-number="426"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L426" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（非エネ起CO2）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">NON_ENERGY_CO2_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L427" class="lines-num"><span id="L427" data-line-number="427"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L427" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（CH4）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">CH4_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L428" class="lines-num"><span id="L428" data-line-number="428"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L428" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（N2O）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">N2O_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L429" class="lines-num"><span id="L429" data-line-number="429"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L429" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（HFC）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">HFC_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L430" class="lines-num"><span id="L430" data-line-number="430"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L430" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（PFC）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">PFC_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L431" class="lines-num"><span id="L431" data-line-number="431"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L431" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（SF6）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">SF6_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L432" class="lines-num"><span id="L432" data-line-number="432"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L432" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">排出係数（NF3）</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">NF3_EMISSION_COEF</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L433" class="lines-num"><span id="L433" data-line-number="433"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L433" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">変換値１</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">CONVERSION_VALUE1</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L434" class="lines-num"><span id="L434" data-line-number="434"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L434" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">変換値２</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">CONVERSION_VALUE2</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L435" class="lines-num"><span id="L435" data-line-number="435"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L435" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">非エネルギー区分</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">NON_ENERGY_KBN</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L436" class="lines-num"><span id="L436" data-line-number="436"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L436" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">温対法フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">GLOBAL_WARMING_LAW_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L437" class="lines-num"><span id="L437" data-line-number="437"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L437" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">省エネ法フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ENERGY_EFFICIENCY_LAW_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L438" class="lines-num"><span id="L438" data-line-number="438"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L438" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目選択画面表示フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ACTIVITY_ITEM_SCREEN_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L439" class="lines-num"><span id="L439" data-line-number="439"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L439" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">補助画面表示区分</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">SUPPORT_SCREEN_KBN</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L440" class="lines-num"><span id="L440" data-line-number="440"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L440" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">単位入力可否フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">UNIT_INPUT_ENABLED_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L441" class="lines-num"><span id="L441" data-line-number="441"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L441" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">換算係数入力可否フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">CONVERSION_COEF_INPUT_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L442" class="lines-num"><span id="L442" data-line-number="442"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L442" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">使用量入力可否フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">USAGE_INPUT_ENABLED_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L443" class="lines-num"><span id="L443" data-line-number="443"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L443" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">販売副生入力可否フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">BY_PRODUCT_INPUT_ENABLED_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L444" class="lines-num"><span id="L444" data-line-number="444"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L444" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">購入未利用熱入力可否フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">UNUSED_HEAT_INPUT_ENABLED_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L445" class="lines-num"><span id="L445" data-line-number="445"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L445" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動量最大値</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ACTIVITY_MAX_LIMIT</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L446" class="lines-num"><span id="L446" data-line-number="446"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L446" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動量最小値</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ACTIVITY_MIN_LIMIT</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L447" class="lines-num"><span id="L447" data-line-number="447"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L447" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">活動項目コメント</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ACTIVITY_ITEM_COMMENT</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L448" class="lines-num"><span id="L448" data-line-number="448"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L448" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">熱関係補助画面表示フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">HEAT_SUPPORT_SCREEN_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L449" class="lines-num"><span id="L449" data-line-number="449"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L449" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">電気関係補助画面表示フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">ELECTRICITY_SUPPORT_SCREEN_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L450" class="lines-num"><span id="L450" data-line-number="450"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L450" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">化石・非化石区分</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">NON_FOSSIL_KBN</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L451" class="lines-num"><span id="L451" data-line-number="451"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L451" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">自家発電（他事業所からの供給）画面表示フラグ</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">SELF_GENERATION_SCREEN_FLAG</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L452" class="lines-num"><span id="L452" data-line-number="452"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L452" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">表示順</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">DISPLAY_ORDER</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L453" class="lines-num"><span id="L453" data-line-number="453"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L453" class="lines-code chroma"><code class="code-inner">    <span class="p">}</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L454" class="lines-num"><span id="L454" data-line-number="454"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L454" class="lines-code chroma"><code class="code-inner">    <span class="c1"># MINOR_CATEGORY_NMが「都市ガス」かつCONVERSION_COEFが空（NaN）の場合、40.00を設定</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L455" class="lines-num"><span id="L455" data-line-number="455"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L455" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span><span class="o">.</span><span class="n">loc</span><span class="p">[</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L456" class="lines-num"><span id="L456" data-line-number="456"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L456" class="lines-code chroma"><code class="code-inner">        <span class="p">(</span><span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">MINOR_CATEGORY_NM</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">==</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">都市ガス</span><span class="s2">&#34;</span><span class="p">)</span> <span class="o">&amp;</span> <span class="p">(</span><span class="n">result_df</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">CONVERSION_COEF</span><span class="s2">&#34;</span><span class="p">]</span><span class="o">.</span><span class="n">isna</span><span class="p">(</span><span class="p">)</span><span class="p">)</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L457" class="lines-num"><span id="L457" data-line-number="457"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L457" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">CONVERSION_COEF</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L458" class="lines-num"><span id="L458" data-line-number="458"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L458" class="lines-code chroma"><code class="code-inner">    <span class="p">]</span> <span class="o">=</span> <span class="mi">40</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L459" class="lines-num"><span id="L459" data-line-number="459"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L459" class="lines-code chroma"><code class="code-inner">    <span class="c1"># &#34;削除フラグ&#34; 列を削除</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L460" class="lines-num"><span id="L460" data-line-number="460"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L460" class="lines-code chroma"><code class="code-inner">    <span class="n">result_df</span> <span class="o">=</span> <span class="n">result_df</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L461" class="lines-num"><span id="L461" data-line-number="461"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L461" class="lines-code chroma"><code class="code-inner">    <span class="c1"># excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L462" class="lines-num"><span id="L462" data-line-number="462"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L462" class="lines-code chroma"><code class="code-inner">    <span class="n">set_system_column</span><span class="p">(</span><span class="n">result_df</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L463" class="lines-num"><span id="L463" data-line-number="463"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L463" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L464" class="lines-num"><span id="L464" data-line-number="464"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L464" class="lines-code chroma"><code class="code-inner">    <span class="c1"># CSVに出力</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L465" class="lines-num"><span id="L465" data-line-number="465"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L465" class="lines-code chroma"><code class="code-inner">    <span class="c1"># result_df.to_csv(&#34;activity_minor_category.csv&#34;, index=False)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L466" class="lines-num"><span id="L466" data-line-number="466"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L466" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L467" class="lines-num"><span id="L467" data-line-number="467"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L467" class="lines-code chroma"><code class="code-inner">    <span class="k">return</span> <span class="n">result_df</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L468" class="lines-num"><span id="L468" data-line-number="468"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L468" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L469" class="lines-num"><span id="L469" data-line-number="469"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L469" class="lines-code chroma"><code class="code-inner"><span class="k">def</span> <span class="nf">get_industy_classification_mst</span><span class="p">(</span><span class="n">excel_file</span><span class="p">)</span><span class="p">:</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L470" class="lines-num"><span id="L470" data-line-number="470"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L470" class="lines-code chroma"><code class="code-inner">    <span class="sa"></span><span class="s2">&#34;&#34;&#34;</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L471" class="lines-num"><span id="L471" data-line-number="471"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L471" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    日本標準産業分類マスタデータ取得</span><span class="s2">
</span></code></td>
						</tr>
						
						
						<tr>
							<td id="L472" class="lines-num"><span id="L472" data-line-number="472"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L472" class="lines-code chroma"><code class="code-inner"><span class="s2"></span><span class="s2">    </span><span class="s2">&#34;&#34;&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L473" class="lines-num"><span id="L473" data-line-number="473"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L473" class="lines-code chroma"><code class="code-inner">    <span class="c1"># Excelファイルのパス（適宜変更）</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L474" class="lines-num"><span id="L474" data-line-number="474"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L474" class="lines-code chroma"><code class="code-inner">    <span class="n">file_path</span> <span class="o">=</span> <span class="n">excel_file</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L475" class="lines-num"><span id="L475" data-line-number="475"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L475" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L476" class="lines-num"><span id="L476" data-line-number="476"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L476" class="lines-code chroma"><code class="code-inner">    <span class="n">dtype_mapping</span> <span class="o">=</span> <span class="p">{</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L477" class="lines-num"><span id="L477" data-line-number="477"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L477" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類大コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L478" class="lines-num"><span id="L478" data-line-number="478"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L478" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類中コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L479" class="lines-num"><span id="L479" data-line-number="479"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L479" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類小コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L480" class="lines-num"><span id="L480" data-line-number="480"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L480" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類細コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="nb">str</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L481" class="lines-num"><span id="L481" data-line-number="481"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L481" class="lines-code chroma"><code class="code-inner">    <span class="p">}</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L482" class="lines-num"><span id="L482" data-line-number="482"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L482" class="lines-code chroma"><code class="code-inner">    
</code></td>
						</tr>
						
						
						<tr>
							<td id="L483" class="lines-num"><span id="L483" data-line-number="483"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L483" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 各シートをデータフレームとして読み込む</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L484" class="lines-num"><span id="L484" data-line-number="484"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L484" class="lines-code chroma"><code class="code-inner">    <span class="n">df_large</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_excel</span><span class="p">(</span><span class="n">file_path</span><span class="p">,</span> <span class="n">sheet_name</span><span class="o">=</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類大</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">skiprows</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="n">dtype_mapping</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L485" class="lines-num"><span id="L485" data-line-number="485"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L485" class="lines-code chroma"><code class="code-inner">    <span class="n">df_medium</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_excel</span><span class="p">(</span><span class="n">file_path</span><span class="p">,</span> <span class="n">sheet_name</span><span class="o">=</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類中</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">skiprows</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="n">dtype_mapping</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L486" class="lines-num"><span id="L486" data-line-number="486"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L486" class="lines-code chroma"><code class="code-inner">    <span class="n">df_small</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_excel</span><span class="p">(</span><span class="n">file_path</span><span class="p">,</span> <span class="n">sheet_name</span><span class="o">=</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類小</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">skiprows</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="n">dtype_mapping</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L487" class="lines-num"><span id="L487" data-line-number="487"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L487" class="lines-code chroma"><code class="code-inner">    <span class="n">df_detailed</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_excel</span><span class="p">(</span><span class="n">file_path</span><span class="p">,</span> <span class="n">sheet_name</span><span class="o">=</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類細</span><span class="s2">&#34;</span><span class="p">,</span> <span class="n">skiprows</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="n">dtype_mapping</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L488" class="lines-num"><span id="L488" data-line-number="488"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L488" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L489" class="lines-num"><span id="L489" data-line-number="489"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L489" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 削除フラグが 0 のものだけ対象</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L490" class="lines-num"><span id="L490" data-line-number="490"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L490" class="lines-code chroma"><code class="code-inner">    <span class="n">df_large</span> <span class="o">=</span> <span class="n">df_large</span><span class="p">[</span><span class="n">df_large</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L491" class="lines-num"><span id="L491" data-line-number="491"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L491" class="lines-code chroma"><code class="code-inner">    <span class="n">df_medium</span> <span class="o">=</span> <span class="n">df_medium</span><span class="p">[</span><span class="n">df_medium</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L492" class="lines-num"><span id="L492" data-line-number="492"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L492" class="lines-code chroma"><code class="code-inner">    <span class="n">df_small</span> <span class="o">=</span> <span class="n">df_small</span><span class="p">[</span><span class="n">df_small</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L493" class="lines-num"><span id="L493" data-line-number="493"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L493" class="lines-code chroma"><code class="code-inner">    <span class="n">df_detailed</span> <span class="o">=</span> <span class="n">df_detailed</span><span class="p">[</span><span class="n">df_detailed</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">削除フラグ</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L494" class="lines-num"><span id="L494" data-line-number="494"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L494" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L495" class="lines-num"><span id="L495" data-line-number="495"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L495" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 各データフレームを結合</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L496" class="lines-num"><span id="L496" data-line-number="496"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L496" class="lines-code chroma"><code class="code-inner">    <span class="n">df_merged</span> <span class="o">=</span> <span class="n">df_detailed</span><span class="o">.</span><span class="n">merge</span><span class="p">(</span><span class="n">df_small</span><span class="p">,</span> <span class="n">on</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類大コード</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類中コード</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類小コード</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">,</span> <span class="n">how</span><span class="o">=</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">left</span><span class="s2">&#34;</span><span class="p">)</span> \
</code></td>
						</tr>
						
						
						<tr>
							<td id="L497" class="lines-num"><span id="L497" data-line-number="497"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L497" class="lines-code chroma"><code class="code-inner">                        <span class="o">.</span><span class="n">merge</span><span class="p">(</span><span class="n">df_medium</span><span class="p">,</span> <span class="n">on</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類大コード</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類中コード</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">,</span> <span class="n">how</span><span class="o">=</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">left</span><span class="s2">&#34;</span><span class="p">)</span> \
</code></td>
						</tr>
						
						
						<tr>
							<td id="L498" class="lines-num"><span id="L498" data-line-number="498"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L498" class="lines-code chroma"><code class="code-inner">                        <span class="o">.</span><span class="n">merge</span><span class="p">(</span><span class="n">df_large</span><span class="p">,</span> <span class="n">on</span><span class="o">=</span><span class="p">[</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類大コード</span><span class="s2">&#34;</span><span class="p">]</span><span class="p">,</span> <span class="n">how</span><span class="o">=</span><span class="sa"></span><span class="s2">&#34;</span><span class="s2">left</span><span class="s2">&#34;</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L499" class="lines-num"><span id="L499" data-line-number="499"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L499" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L500" class="lines-num"><span id="L500" data-line-number="500"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L500" class="lines-code chroma"><code class="code-inner">    <span class="n">df_result</span> <span class="o">=</span> <span class="n">df_merged</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">{</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L501" class="lines-num"><span id="L501" data-line-number="501"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L501" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類大コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">DIVISION_CODE</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L502" class="lines-num"><span id="L502" data-line-number="502"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L502" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類中コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MAJOR_GROUP_CODE</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L503" class="lines-num"><span id="L503" data-line-number="503"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L503" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類小コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">GROUP_CODE</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L504" class="lines-num"><span id="L504" data-line-number="504"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L504" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類細コード</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">INDUSTRY_CODE</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L505" class="lines-num"><span id="L505" data-line-number="505"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L505" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類大名</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">DIVISION_NAME</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L506" class="lines-num"><span id="L506" data-line-number="506"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L506" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類中名</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MAJOR_GROUP_NAME</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L507" class="lines-num"><span id="L507" data-line-number="507"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L507" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類小名</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">GROUP_NAME</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L508" class="lines-num"><span id="L508" data-line-number="508"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L508" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">産業分類細名</span><span class="s2">&#34;</span><span class="p">:</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">INDUSTRY_NAME</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L509" class="lines-num"><span id="L509" data-line-number="509"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L509" class="lines-code chroma"><code class="code-inner">    <span class="p">}</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L510" class="lines-num"><span id="L510" data-line-number="510"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L510" class="lines-code chroma"><code class="code-inner">    
</code></td>
						</tr>
						
						
						<tr>
							<td id="L511" class="lines-num"><span id="L511" data-line-number="511"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L511" class="lines-code chroma"><code class="code-inner">    <span class="c1"># 必要なカラムを選択</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L512" class="lines-num"><span id="L512" data-line-number="512"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L512" class="lines-code chroma"><code class="code-inner">    <span class="n">df_result</span> <span class="o">=</span> <span class="n">df_result</span><span class="p">[</span><span class="p">[</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L513" class="lines-num"><span id="L513" data-line-number="513"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L513" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">DIVISION_CODE</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MAJOR_GROUP_CODE</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">GROUP_CODE</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">INDUSTRY_CODE</span><span class="s2">&#34;</span><span class="p">,</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L514" class="lines-num"><span id="L514" data-line-number="514"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L514" class="lines-code chroma"><code class="code-inner">        <span class="sa"></span><span class="s2">&#34;</span><span class="s2">DIVISION_NAME</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">MAJOR_GROUP_NAME</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">GROUP_NAME</span><span class="s2">&#34;</span><span class="p">,</span> <span class="sa"></span><span class="s2">&#34;</span><span class="s2">INDUSTRY_NAME</span><span class="s2">&#34;</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L515" class="lines-num"><span id="L515" data-line-number="515"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L515" class="lines-code chroma"><code class="code-inner">    <span class="p">]</span><span class="p">]</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L516" class="lines-num"><span id="L516" data-line-number="516"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L516" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L517" class="lines-num"><span id="L517" data-line-number="517"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L517" class="lines-code chroma"><code class="code-inner">    <span class="c1"># excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L518" class="lines-num"><span id="L518" data-line-number="518"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L518" class="lines-code chroma"><code class="code-inner">    <span class="n">set_system_column</span><span class="p">(</span><span class="n">df_result</span><span class="p">)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L519" class="lines-num"><span id="L519" data-line-number="519"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L519" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L520" class="lines-num"><span id="L520" data-line-number="520"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L520" class="lines-code chroma"><code class="code-inner">    <span class="c1"># CSVに出力</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L521" class="lines-num"><span id="L521" data-line-number="521"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L521" class="lines-code chroma"><code class="code-inner">    <span class="c1"># df_result.to_csv(&#34;industy_classification.csv&#34;, index=False)</span>
</code></td>
						</tr>
						
						
						<tr>
							<td id="L522" class="lines-num"><span id="L522" data-line-number="522"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L522" class="lines-code chroma"><code class="code-inner">
</code></td>
						</tr>
						
						
						<tr>
							<td id="L523" class="lines-num"><span id="L523" data-line-number="523"></span></td>
							
								<td class="lines-escape"></td>
							
							<td rel="L523" class="lines-code chroma"><code class="code-inner">    <span class="k">return</span> <span class="n">df_result</span>
</code></td>
						</tr>
						
					</tbody>
				</table>
				<div class="code-line-menu ui vertical pointing menu tippy-target">
					
						<a class="item ref-in-new-issue" data-url-issue-new="/hd-dev-user01/esg05/issues/new" data-url-param-body-link="/hd-dev-user01/esg05/src/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py" rel="nofollow noindex">新しいイシューから参照</a>
					
					<a class="item view_git_blame" href="/hd-dev-user01/esg05/blame/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py">Git Blameを表示</a>
					<a class="item copy-line-permalink" data-url="/hd-dev-user01/esg05/src/commit/81d9328a5f2a8b9bd976f47f3bd5163081c37afb/dags/middle/report_register/register_public_factor.py">パーマリンクをコピー</a>
				</div>
				
			
		</div>
	</div>
</div>

		
	</div>
</div>


	

	</div>

	

	<footer class="page-footer" role="group" aria-label="フッター">
	<div class="left-links" role="contentinfo" aria-label="ソフトウェアについて">
		<a target="_blank" rel="noopener noreferrer" href="https://about.gitea.com">Powered by Gitea</a>
		
			バージョン:
			
				<a href="/admin/config">1.21.5</a>
			
		
		
			ページ: <strong>633ms</strong>
			テンプレート: <strong>10ms</strong>
		
	</div>
	<div class="right-links" role="group" aria-label="リンク">
		<div class="ui dropdown upward language">
			<span class="flex-text-inline"><svg viewBox="0 0 16 16" class="svg octicon-globe" aria-hidden="true" width="14" height="14"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM5.78 8.75a9.64 9.64 0 0 0 1.363 4.177c.255.426.542.832.857 1.215.245-.296.551-.705.857-1.215A9.64 9.64 0 0 0 10.22 8.75Zm4.44-1.5a9.64 9.64 0 0 0-1.363-4.177c-.307-.51-.612-.919-.857-1.215a9.927 9.927 0 0 0-.857 1.215A9.64 9.64 0 0 0 5.78 7.25Zm-5.944 1.5H1.543a6.507 6.507 0 0 0 4.666 5.5c-.123-.181-.24-.365-.352-.552-.715-1.192-1.437-2.874-1.581-4.948Zm-2.733-1.5h2.733c.144-2.074.866-3.756 1.58-4.948.12-.197.237-.381.353-.552a6.507 6.507 0 0 0-4.666 5.5Zm10.181 1.5c-.144 2.074-.866 3.756-1.58 4.948-.12.197-.237.381-.353.552a6.507 6.507 0 0 0 4.666-5.5Zm2.733-1.5a6.507 6.507 0 0 0-4.666-5.5c.123.181.24.365.353.552.714 1.192 1.436 2.874 1.58 4.948Z"/></svg> 日本語</span>
			<div class="menu language-menu">
				
					<a lang="id-ID" data-url="/?lang=id-ID" class="item ">Bahasa Indonesia</a>
				
					<a lang="de-DE" data-url="/?lang=de-DE" class="item ">Deutsch</a>
				
					<a lang="en-US" data-url="/?lang=en-US" class="item ">English</a>
				
					<a lang="es-ES" data-url="/?lang=es-ES" class="item ">Español</a>
				
					<a lang="fr-FR" data-url="/?lang=fr-FR" class="item ">Français</a>
				
					<a lang="it-IT" data-url="/?lang=it-IT" class="item ">Italiano</a>
				
					<a lang="lv-LV" data-url="/?lang=lv-LV" class="item ">Latviešu</a>
				
					<a lang="hu-HU" data-url="/?lang=hu-HU" class="item ">Magyar nyelv</a>
				
					<a lang="nl-NL" data-url="/?lang=nl-NL" class="item ">Nederlands</a>
				
					<a lang="pl-PL" data-url="/?lang=pl-PL" class="item ">Polski</a>
				
					<a lang="pt-PT" data-url="/?lang=pt-PT" class="item ">Português de Portugal</a>
				
					<a lang="pt-BR" data-url="/?lang=pt-BR" class="item ">Português do Brasil</a>
				
					<a lang="fi-FI" data-url="/?lang=fi-FI" class="item ">Suomi</a>
				
					<a lang="sv-SE" data-url="/?lang=sv-SE" class="item ">Svenska</a>
				
					<a lang="tr-TR" data-url="/?lang=tr-TR" class="item ">Türkçe</a>
				
					<a lang="cs-CZ" data-url="/?lang=cs-CZ" class="item ">Čeština</a>
				
					<a lang="el-GR" data-url="/?lang=el-GR" class="item ">Ελληνικά</a>
				
					<a lang="bg-BG" data-url="/?lang=bg-BG" class="item ">Български</a>
				
					<a lang="ru-RU" data-url="/?lang=ru-RU" class="item ">Русский</a>
				
					<a lang="uk-UA" data-url="/?lang=uk-UA" class="item ">Українська</a>
				
					<a lang="fa-IR" data-url="/?lang=fa-IR" class="item ">فارسی</a>
				
					<a lang="ml-IN" data-url="/?lang=ml-IN" class="item ">മലയാളം</a>
				
					<a lang="ja-JP" data-url="/?lang=ja-JP" class="item active selected">日本語</a>
				
					<a lang="zh-CN" data-url="/?lang=zh-CN" class="item ">简体中文</a>
				
					<a lang="zh-TW" data-url="/?lang=zh-TW" class="item ">繁體中文（台灣）</a>
				
					<a lang="zh-HK" data-url="/?lang=zh-HK" class="item ">繁體中文（香港）</a>
				
					<a lang="ko-KR" data-url="/?lang=ko-KR" class="item ">한국어</a>
				
			</div>
		</div>
		<a href="/assets/licenses.txt">ライセンス</a>
		<a href="/api/swagger">API</a>
		
	</div>
</footer>




	<script src="/assets/js/index.js?v=1.21.5" onerror="alert('Failed to load asset files from ' + this.src + '. Please make sure the asset files can be accessed.')"></script>

	
	
</body>
</html>
