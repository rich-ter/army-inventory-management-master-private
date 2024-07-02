/*
Template Name: HUD DJANGO - Responsive Bootstrap 5 Admin Template
Version: 1.0.0
Author: Sean Ngu
Website: http://www.seantheme.com/hud-django/
	----------------------------
		APPS CONTENT TABLE
	----------------------------

	<!-- ======== GLOBAL SCRIPT SETTING ======== -->
  01. Global Variable
  02. Handle Scrollbar
  03. Handle Sidebar Menu
  04. Handle Sidebar Scroll Memory
  05. Handle Card Action
  06. Handle Tooltip & Popover Activation
  07. Handle Scroll to Top Button
  08. Handle hexToRgba
  09. Handle Scroll To
  10. Handle Toggle Class
  11. Handle Theme Panel
	12. Handle CSS Variable
	13. Handle Top Menu - Unlimited Top Menu Render
  14. Initialise
  15. Handle Top Nav - Mobile Top Menu Toggle
	16. Animation - Slide Up
	17. Animation - Slide Down
	18. Animation - Slide Toggle
	19. Application Controller
	20. Initialise
	
	<!-- ======== APPLICATION SETTING ======== -->
	Application Controller
*/



/* 01. Global Variable
------------------------------------------------ */
var app = {
	id: '#app',
	isMobile: ((/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) || window.innerWidth < 992),
	bootstrap: {
		tooltip: {
			attr: 'data-bs-toggle="tooltip"'
		},
		popover: {
			attr: 'data-bs-toggle="popover"'
		},
		modal: {
			attr: 'data-bs-toggle="modal"',
			dismissAttr: 'data-bs-dismiss="modal"',
			event: {
				hidden: 'hidden.bs.modal'
			}
		},
		nav: {
			class: 'nav',
			tabs: {
				class: 'nav-tabs',
				activeClass: 'active',
				itemClass: 'nav-item',
				itemLinkClass: 'nav-link'
			}
		}
	},
	header: {
		id: '#header',
		class: 'app-header',
		hasScrollClass: 'has-scroll'
	},
	sidebar: {
		id: '#sidebar',
		class: 'app-sidebar',
		scrollBar: {
			localStorage: 'appSidebarScrollPosition',
			dom: ''
		},
		menu: {
			class: 'menu',
			initAttr: 'data-init',
			animationTime: 0,
			itemClass: 'menu-item',
			itemLinkClass: 'menu-link',
			hasSubClass: 'has-sub',
			activeClass: 'active',
			expandingClass: 'expanding',
			expandClass: 'expand',
			submenu: {
				class: 'menu-submenu',
			}
		},
		mobile: {
			toggleAttr: 'data-toggle="app-sidebar-mobile"',
			dismissAttr: 'data-dismiss="app-sidebar-mobile"',
			toggledClass: 'app-sidebar-mobile-toggled',
			closedClass: 'app-sidebar-mobile-closed',
			backdrop: {
				class: 'app-sidebar-mobile-backdrop'
			}
		},
		minify: {
			toggleAttr: 'data-toggle="app-sidebar-minify"',
			toggledClass: 'app-sidebar-minified',
			cookieName: 'app-sidebar-minified'
		},
		floatSubmenu: {
			id: '#app-sidebar-float-submenu',
			dom: '',
			timeout: '',
			class: 'app-sidebar-float-submenu',
			container: {
				class: 'app-sidebar-float-submenu-container'
			},
			arrow: {
				id: '#app-sidebar-float-submenu-arrow',
				class: 'app-sidebar-float-submenu-arrow'
			},
			line: {
				id: '#app-sidebar-float-submenu-line',
				class: 'app-sidebar-float-submenu-line'
			},
			overflow: {
				class: 'overflow-scroll mh-100vh'
			}
		},
		search: {
			class: 'menu-search',
			toggleAttr: 'data-sidebar-search="true"',
			hideClass: 'd-none',
			foundClass: 'has-text'
		},
		transparent: {
			class: 'app-sidebar-transparent'
		}
	},
	topNav: {
		id: '#top-nav',
		class: 'app-top-nav',
		mobile: {
			toggleAttr: 'data-toggle="app-top-nav-mobile"'
		},
		menu: {
			class: 'menu',
			itemClass: 'menu-item',
			itemLinkClass: 'menu-link',
			activeClass: 'active',
			hasSubClass: 'has-sub',
			expandClass: 'expand',
			submenu: {
				class: 'menu-submenu'
			}
		},
		control: {
			class: 'menu-control',
			startClass: 'menu-control-start',
			endClass: 'menu-control-end',
			showClass: 'show',
			buttonPrev: {
				class: 'menu-control-start',
				toggleAttr: 'data-toggle="app-top-menu-prev"'
			},
			buttonNext: {
				class: 'menu-control-end',
				toggleAttr: 'data-toggle="app-top-menu-next"'
			}
		}
	},
	scrollBar: {
		attr: 'data-scrollbar="true"',
		skipMobileAttr: 'data-skip-mobile',
		heightAttr: 'data-height',
		wheelPropagationAttr: 'data-wheel-propagation'
	},
	content: {
		id: '#content',
		class: 'app-content',
		fullHeight: {
			class: 'app-content-full-height'
		},
		fullWidth: {
			class: 'app-content-full-width'
		}
	},
	layout: {
		sidebarLight: {
			class: 'app-with-light-sidebar'
		},
		sidebarEnd: {
			class: 'app-with-end-sidebar'
		},
		sidebarWide: {
			class: 'app-with-wide-sidebar'
		},
		sidebarMinified: {
			class: 'app-sidebar-minified'
		},
		sidebarTwo: {
			class: 'app-with-two-sidebar'
		},
		withoutHeader: {
			class: 'app-without-header'
		},
		withoutSidebar: {
			class: 'app-without-sidebar'
		},
		topMenu: {
			class: 'app-with-top-menu'
		},
		boxedLayout: {
			class: 'boxed-layout'
		}
	},
	scrollToTopBtn: {
		showClass: 'show',
		heightShow: 200,
		toggleAttr: 'data-toggle="scroll-to-top"',
		scrollSpeed: 500
	},
	scrollTo: {
		attr: 'data-toggle="scroll-to"',
		target: 'data-target',
		linkTarget: 'href'
	},
	themePanel: {
		class: 'app-theme-panel',
		toggleAttr: 'data-toggle="theme-panel-expand"',
		cookieName: 'app-theme-panel-expand',
		activeClass: 'active',
		themeListCLass: 'app-theme-list',
		themeListItemCLass: 'app-theme-list-item',
		themeCoverClass: 'app-theme-cover',
		themeCoverItemClass: 'app-theme-cover-item',
		theme: {
			toggleAttr: 'data-toggle="theme-selector"',
			classAttr: 'data-theme-class',
			cookieName: 'app-theme',
			activeClass: 'active'
		},
		themeCover: {
			toggleAttr: 'data-toggle="theme-cover-selector"',
			classAttr: 'data-theme-cover-class',
			cookieName: 'app-theme-cover',
			activeClass: 'active'
		},
		themeMode: {
			toggleAttr: 'data-toggle="theme-mode-selector"',
			valueAttr: 'data-theme-mode',
			cookieName: 'app-theme-mode',
			activeClass: 'active',
			attr: 'data-bs-theme'
		}
	},
	dismissClass: {
		toggleAttr: 'data-dismiss-class',
		targetAttr: 'data-dismiss-target'
	},
	toggleClass: {
		toggleAttr: 'data-toggle-class',
		targetAttr: 'data-toggle-target'
	},
	variablePrefix: 'bs-',
	variableFontList: ['body-font-family', 'body-font-size', 'body-font-weight', 'body-line-height'],
	variableColorList: [
		'theme', 'theme-rgb', 'theme-color', 'theme-color-rgb',
		'default', 'default-rgb',
		'primary', 'primary-rgb', 'primary-bg-subtle', 'primary-text', 'primary-border-subtle',
		'secondary', 'secondary-rgb', 'secondary-bg-subtle', 'secondary-text', 'secondary-border-subtle',
		'success', 'success-rgb', 'success-bg-subtle', 'success-text', 'success-border-subtle',
		'warning', 'warning-rgb', 'warning-bg-subtle', 'warning-text', 'warning-border-subtle',
		'info', 'info-rgb', 'info-bg-subtle', 'info-text', 'info-border-subtle',
		'danger', 'danger-rgb', 'danger-bg-subtle', 'danger-text', 'danger-border-subtle',
		'light', 'light-rgb', 'light-bg-subtle', 'light-text', 'light-border-subtle',
		'dark', 'dark-rgb', 'dark-bg-subtle', 'dark-text', 'dark-border-subtle',
		'inverse', 'inverse-rgb',
		'white', 'white-rgb',
		'black', 'black-rgb',
		'teal', 'teal-rgb',
		'indigo', 'indigo-rgb', 
		'purple', 'purple-rgb',
		'yellow', 'yellow-rgb',
		'pink', 'pink-rgb',
		'cyan', 'cyan-rgb',
		'gray-100', 'gray-200', 'gray-300', 'gray-400', 'gray-500',  'gray-600', 'gray-700', 'gray-800', 'gray-900', 
		'gray-100-rgb', 'gray-200-rgb', 'gray-300-rgb', 'gray-400-rgb', 'gray-500-rgb',  'gray-600-rgb', 'gray-700-rgb', 'gray-800-rgb', 'gray-900-rgb', 
		'muted', 'muted-rgb', 'emphasis-color', 'emphasis-color-rgb',
		'body-bg', 'body-bg-rgb', 'body-color', 'body-color-rgb',
		'heading-color', 
		'secondary-color', 'secondary-color-rgb', 'secondary-bg', 'secondary-bg-rgb',
		'tertiary-color', 'tertiary-color-rgb', 'tertiary-bg', 'tertiary-bg-rgb',
		'link-color', 'link-color-rgb', 'link-hover-color', 'link-hover-color-rgb', 
		'border-color', 'border-color-translucent'
	],
	font: {},
	color: {},
	card: {
		expand: {
			status: false,
			toggleAttr: 'data-toggle="card-expand"',
			toggleTitle: 'Expand / Compress',
			class: 'card-expand'
		}
	},
	init: {
		attr: 'data-init',
		class: 'app-init'
	},
	animation: {
		attr: 'data-animation',
		valueAttr: 'data-value',
		speed: 300,
		effect: 'swing'
	},
	breakpoints: {
		xs: 0,
		sm: 576,
		md: 768,
		lg: 992,
		xl: 1200,
		xxl: 1660,
		xxxl: 1900
	}
};



/* 02. Handle Scrollbar
------------------------------------------------ */
var handleScrollbar = function() {
	"use strict";
	var elms = document.querySelectorAll('['+ app.scrollBar.attr +']');
		
	for (var i = 0; i < elms.length; i++) {
		generateScrollbar(elms[i])
	}
};
var generateScrollbar = function(elm) {
  "use strict";
	
	if (elm.scrollbarInit || (app.isMobile && elm.getAttribute(app.scrollBar.skipMobileAttr))) {
		return;
	}
	var dataHeight = (!elm.getAttribute(app.scrollBar.heightAttr)) ? elm.offsetHeight : elm.getAttribute(app.scrollBar.heightAttr);
	
	elm.style.height = dataHeight;
	elm.scrollbarInit = true;
	
	if(app.isMobile) {
		elm.style.overflowX = 'scroll';
	} else {
		var dataWheelPropagation = (elm.getAttribute(app.scrollBar.wheelPropagationAttr)) ? elm.getAttribute(app.scrollBar.wheelPropagationAttr) : false;
		
		if (elm.closest('.'+ app.sidebar.class) && elm.closest('.'+ app.sidebar.class).length !== 0) {
			app.sidebar.scrollBar.dom = new PerfectScrollbar(elm, {
				wheelPropagation: dataWheelPropagation
			});
		} else {
			new PerfectScrollbar(elm, {
				wheelPropagation: dataWheelPropagation
			});
		}
	}
	elm.setAttribute(app.init.attr, true);
	elm.classList.remove('invisible');
};



/* 03. Handle Sidebar Menu
------------------------------------------------ */
var handleSidebarMenuToggle = function(menus) {
	menus.map(function(menu) {
		menu.onclick = function(e) {
			e.preventDefault();
			var target = this.nextElementSibling;
	
			menus.map(function(m) {
				var otherTarget = m.nextElementSibling;
				if (otherTarget !== target) {
					otherTarget.style.display = 'none';
					otherTarget.closest('.'+ app.sidebar.menu.itemClass).classList.remove(app.sidebar.menu.expandClass);
				}
			});
	
			var targetItemElm = target.closest('.'+ app.sidebar.menu.itemClass);

			if (targetItemElm.classList.contains(app.sidebar.menu.expandClass) || (targetItemElm.classList.contains(app.sidebar.menu.activeClass) && !target.style.display)) {
				targetItemElm.classList.remove(app.sidebar.menu.expandClass);
				target.style.display = 'none';
			} else {
				targetItemElm.classList.add(app.sidebar.menu.expandClass);
				target.style.display = 'block';
			}
		}
	});
};
var handleSidebarMenu = function() {
	"use strict";
	
	var menuBaseSelector = '.'+ app.sidebar.class +' .'+ app.sidebar.menu.class +' > .'+ app.sidebar.menu.itemClass +'.'+ app.sidebar.menu.hasSubClass;
	var submenuBaseSelector = ' > .'+ app.sidebar.menu.submenu.class +' > .'+ app.sidebar.menu.itemClass + '.' + app.sidebar.menu.hasSubClass;
	
	// menu
	var menuLinkSelector =  menuBaseSelector + ' > .'+ app.sidebar.menu.itemLinkClass;
	var menus = [].slice.call(document.querySelectorAll(menuLinkSelector));
	handleSidebarMenuToggle(menus);
	
	// submenu lvl 1
	var submenuLvl1Selector = menuBaseSelector + submenuBaseSelector;
	var submenusLvl1 = [].slice.call(document.querySelectorAll(submenuLvl1Selector + ' > .' + app.sidebar.menu.itemLinkClass));
	handleSidebarMenuToggle(submenusLvl1);
	
	// submenu lvl 2
	var submenuLvl2Selector = menuBaseSelector + submenuBaseSelector + submenuBaseSelector;
	var submenusLvl2 = [].slice.call(document.querySelectorAll(submenuLvl2Selector + ' > .' + app.sidebar.menu.itemLinkClass));
	handleSidebarMenuToggle(submenusLvl2);
};



/* 04. Handle Sidebar Scroll Memory
------------------------------------------------ */
var handleSidebarScrollMemory = function() {
	if (!app.isMobile) {
		try {
			if (typeof(Storage) !== 'undefined' && typeof(localStorage) !== 'undefined') {
				var elm = document.querySelector('.'+ app.sidebar.class +' ['+ app.scrollBar.attr +']');
				
				if (elm) {
					elm.onscroll = function() {
						localStorage.setItem(app.sidebar.scrollBar.localStorage, this.scrollTop);
					}
					var defaultScroll = localStorage.getItem(app.sidebar.scrollBar.localStorage);
					if (defaultScroll) {
						document.querySelector('.'+ app.sidebar.class +' ['+ app.scrollBar.attr +']').scrollTop = defaultScroll;
					}
				}
			}
		} catch (error) {
			console.log(error);
		}
	}
};



/* 05. Handle Card Action
------------------------------------------------ */
var handleCardAction = function() {
	"use strict";

	if (app.card.expand.status) {
		return false;
	}
	app.card.expand.status = true;

	// expand
	var expandTogglerList = [].slice.call(document.querySelectorAll('['+ app.card.expand.toggleAttr +']'));
	var expandTogglerTooltipList = expandTogglerList.map(function (expandTogglerEl) {
		expandTogglerEl.onclick = function(e) {
			e.preventDefault();
		
			var target = this.closest('.card');
			var targetClass = app.card.expand.class;
			var targetTop = 40;

			if (document.body.classList.contains(targetClass) && target.classList.contains(targetClass)) {
				target.removeAttribute('style');
				target.classList.remove(targetClass);
				document.body.classList.remove(targetClass);
			} else {
				document.body.classList.add(targetClass);
				target.classList.add(targetClass);
			}
		
			window.dispatchEvent(new Event('resize'));
		};
	
		return new bootstrap.Tooltip(expandTogglerEl, {
			title: app.card.expand.toggleTitle,
			placement: 'bottom',
			trigger: 'hover',
			container: 'body'
		});
	});
};



/* 06. Handle Tooltip & Popover Activation
------------------------------------------------ */
var handelTooltipPopoverActivation = function() {
	"use strict";
	
	var tooltipTriggerList = [].slice.call(document.querySelectorAll('['+ app.bootstrap.tooltip.attr +']'))
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
		return new bootstrap.Tooltip(tooltipTriggerEl);
	});
	
	var popoverTriggerList = [].slice.call(document.querySelectorAll('['+ app.bootstrap.popover.attr +']'))
	var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
		return new bootstrap.Popover(popoverTriggerEl);
	});
};



/* 07. Handle Scroll to Top Button
------------------------------------------------ */
var handleScrollToTopButton = function() {
	"use strict";
	
	var elmTriggerList = [].slice.call(document.querySelectorAll('['+ app.scrollToTopBtn.toggleAttr +']'));
	
	document.onscroll = function() {
		var doc = document.documentElement;
		var totalScroll = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0);
		var elmList = elmTriggerList.map(function(elm) {
			if (totalScroll >= app.scrollToTopBtn.heightShow) {
				if (!elm.classList.contains(app.scrollToTopBtn.showClass)) {
					elm.classList.add(app.scrollToTopBtn.showClass);
				}
			} else {
				elm.classList.remove(app.scrollToTopBtn.showClass);
			}
		});
		
		var elm = document.querySelectorAll(app.id)[0];
		
		if (elm) {
			if (totalScroll > 0) {
				elm.classList.add(app.header.hasScrollClass);
			} else {
				elm.classList.remove(app.header.hasScrollClass);
			}
		}
	}
	
	var elmList = elmTriggerList.map(function(elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			
			window.scrollTo({top: 0, behavior: 'smooth'});
		}
	});
};



/* 08. Handle hexToRgba
------------------------------------------------ */
var hexToRgba = function(hex, transparent = 1) {
	var c;
	if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
		c= hex.substring(1).split('');
		if(c.length== 3){
				c= [c[0], c[0], c[1], c[1], c[2], c[2]];
		}
		c= '0x'+c.join('');
		return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+','+ transparent +')';
	}
  throw new Error('Bad Hex');
};



/* 09. Handle Scroll To
------------------------------------------------ */
var handleScrollTo = function() {
	var elmTriggerList = [].slice.call(document.querySelectorAll('['+ app.scrollTo.attr +']'));
	var elmList = elmTriggerList.map(function(elm) {
		elm.onclick = function(e) {
			e.preventDefault();
		
			var targetAttr = (elm.getAttribute(app.scrollTo.target)) ? this.getAttribute(app.scrollTo.target) : this.getAttribute(app.scrollTo.linkTarget);
			var targetElm = document.querySelectorAll(targetAttr)[0];
			var targetHeader = document.querySelectorAll(app.header.id)[0];
			var targetHeight = targetHeader.offsetHeight;
			if (targetElm) {
				var targetTop = targetElm.offsetTop - targetHeight - 24;
				window.scrollTo({top: targetTop, behavior: 'smooth'});
			}
		}
	});
};



/* 10. Handle Toggle Class
------------------------------------------------ */
var handleToggleClass = function() {
	var elmList = [].slice.call(document.querySelectorAll('['+ app.toggleClass.toggleAttr +']'));
	
	elmList.map(function(elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			
			var targetToggleClass = this.getAttribute(app.toggleClass.toggleAttr);
			var targetDismissClass = this.getAttribute(app.dismissClass.toggleAttr);
			var targetToggleElm = document.querySelector(this.getAttribute(app.toggleClass.targetAttr));
		
			if (!targetDismissClass) {
				if (targetToggleElm.classList.contains(targetToggleClass)) {
					targetToggleElm.classList.remove(targetToggleClass);
				} else {
					targetToggleElm.classList.add(targetToggleClass);
				}
			} else {
				if (!targetToggleElm.classList.contains(targetToggleClass) && !targetToggleElm.classList.contains(targetDismissClass)) {
					if (targetToggleElm.classList.contains(targetToggleClass)) {
						targetToggleElm.classList.remove(targetToggleClass);
					} else {
						targetToggleElm.classList.add(targetToggleClass);
					}
				} else {
					if (targetToggleElm.classList.contains(targetToggleClass)) {
						targetToggleElm.classList.remove(targetToggleClass);
					} else {
						targetToggleElm.classList.add(targetToggleClass);
					}
					if (targetToggleElm.classList.contains(targetDismissClass)) {
						targetToggleElm.classList.remove(targetDismissClass);
					} else {
						targetToggleElm.classList.add(targetDismissClass);
					}
				}
			}
		}
	});
}



/* 11. Handle Theme Panel
------------------------------------------------ */
var handleThemePanel = function() {
	"use strict";
	
	// 12.1 Theme Panel - Toggle / Dismiss
	var elmList = [].slice.call(document.querySelectorAll('['+ app.themePanel.toggleAttr +']'));
	
	elmList.map(function(elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			
			var targetContainer = document.querySelector('.'+ app.themePanel.class);
			var targetExpand = false;
		
			if (targetContainer.classList.contains(app.themePanel.activeClass)) {
				targetContainer.classList.remove(app.themePanel.activeClass);
			} else {
				targetContainer.classList.add(app.themePanel.activeClass);
				targetExpand = true;
			}
			if (Cookies) {
				Cookies.set(app.themePanel.cookieName, targetExpand);
			}
		}
	});
	
	// 12.2 Theme Panel - Page Load Cookies 
	if (Cookies) {
		var themePanelExpand = Cookies.get(app.themePanel.cookieName);
		
		if (themePanelExpand == 'true' || typeof themePanelExpand == 'undefined') {
			var elm = document.querySelector('['+ app.themePanel.toggleAttr +']');
			if (elm) {
				elm.click();
			}
		}
	}
	
	
	// 12.3 Theme Panel - Theme Selector
	var elmList = [].slice.call(document.querySelectorAll('.'+ app.themePanel.class +' ['+ app.themePanel.theme.toggleAttr +']'));
	elmList.map(function(elm) {
		elm.onclick = function() {
			for (var x = 0; x < document.body.classList.length; x++) {
				var targetClass = document.body.classList[x];
				if (targetClass.search('theme-') > -1) {
					document.body.classList.remove(targetClass);
				}
			}
		
			var targetTheme = this.getAttribute(app.themePanel.theme.classAttr);
			var targetThemeList = [].slice.call(document.querySelectorAll('.'+ app.themePanel.class +' ['+ app.themePanel.theme.toggleAttr +']'));
			
			if (targetTheme) {
				document.body.classList.add(targetTheme);
			}
			targetThemeList.map(function(targetElm) {
				if (targetElm.getAttribute(app.themePanel.theme.classAttr) != targetTheme) {
					targetElm.closest('.'+ app.themePanel.themeListItemCLass).classList.remove(app.themePanel.theme.activeClass);
				}
			});
			
			this.closest('.'+ app.themePanel.themeListItemCLass).classList.add(app.themePanel.theme.activeClass);
			
			if (Cookies) {
				Cookies.set(app.themePanel.theme.cookieName, targetTheme);
				app.color.theme = (getComputedStyle(document.body).getPropertyValue('--bs-theme')).trim();
				app.color.themeRgb = (getComputedStyle(document.body).getPropertyValue('--bs-theme-rgb')).trim();
				
				document.dispatchEvent(new Event('theme-reload'));
			}
		}
	});
	
	if (Cookies) {
		if (Cookies.get(app.themePanel.theme.cookieName)) {
			var targetElm = document.querySelector('.'+ app.themePanel.class +' ['+ app.themePanel.theme.toggleAttr +']' + '['+ app.themePanel.theme.classAttr +'="'+ Cookies.get(app.themePanel.theme.cookieName) +'"]');
			
			if (targetElm) {
				targetElm.click();
			
				app.color.theme = (getComputedStyle(document.body).getPropertyValue('--bs-theme')).trim();
				app.color.themeRgb = (getComputedStyle(document.body).getPropertyValue('--bs-theme-rgb')).trim();
			
				document.dispatchEvent(new Event('theme-reload'));
			}
		}
	}
	
	
	// 12.4 Theme Panel - Background Selector
	var elmList = [].slice.call(document.querySelectorAll('.'+ app.themePanel.class +' ['+ app.themePanel.themeCover.toggleAttr +']'));
	elmList.map(function(elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			
			var htmlElm = document.querySelector('html');
			var targetTheme = this.getAttribute(app.themePanel.themeCover.classAttr);
			for (var x = 0; x < document.documentElement.classList.length; x++) {
				var targetClass = document.documentElement.classList[x];
				if (targetClass.search('bg-cover-') > -1) {
					htmlElm.classList.remove(targetClass);
				}
			}
			
			if (targetTheme) {
				htmlElm.classList.add(targetTheme);
			}
			
			var targetCoverList = [].slice.call(document.querySelectorAll('.'+ app.themePanel.class +' ['+ app.themePanel.themeCover.toggleAttr +']'));
			targetCoverList.map(function(targetElm) {
				if (targetElm.getAttribute(app.themePanel.themeCover.toggleAttr) != targetTheme) {
					targetElm.closest('.'+ app.themePanel.themeCoverItemClass).classList.remove(app.themePanel.themeCover.activeClass);
				}
			});
			
			this.closest('.'+ app.themePanel.themeCoverItemClass).classList.add(app.themePanel.themeCover.activeClass);
			if (Cookies) {
				Cookies.set(app.themePanel.themeCover.cookieName, targetTheme);
			}
		};
	});
	
	if (Cookies) {
		if (Cookies.get(app.themePanel.themeCover.cookieName)) {
			var targetElm = document.querySelector('.'+ app.themePanel.class +' ['+ app.themePanel.themeCover.toggleAttr +']' + '['+ app.themePanel.themeCover.classAttr +'="'+ Cookies.get(app.themePanel.themeCover.cookieName) +'"]');
			if (targetElm) {
				targetElm.click();
			}
		}
	}
	
	
	// 12.5 Theme Panel - Mode Selector
	var elms = [].slice.call(document.querySelectorAll('.'+ app.themePanel.class +' ['+ app.themePanel.themeMode.toggleAttr +']'));
	elms.map(function(elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			
			var targetElm = this;
			var targetMode = (targetElm.getAttribute(app.themePanel.themeMode.valueAttr)) ? targetElm.getAttribute(app.themePanel.themeMode.valueAttr) : '';
		
			if (targetMode == 'dark') {
				document.querySelector('html').setAttribute(app.themePanel.themeMode.attr, targetMode);
			} else {
				document.querySelector('html').removeAttribute(app.themePanel.themeMode.attr);
			}
			if (Cookies) {
				Cookies.set(app.themePanel.themeMode.cookieName, targetMode);
			}
			targetElm.classList.add(app.themePanel.themeMode.activeClass);
			
			var elms2 = [].slice.call(document.querySelectorAll('.'+ app.themePanel.class +' ['+ app.themePanel.themeMode.toggleAttr +']'));
			elms2.map(function(elm2) {
				if (elm2 != targetElm) {
					elm2.classList.remove(app.themePanel.themeMode.activeClass);
				}
			});
			
			handleCssVariable();
			document.dispatchEvent(new CustomEvent('theme-reload'));
		}
	});
	
	if (Cookies) {
		if (Cookies.get(app.themePanel.themeMode.cookieName)) {
			var targetElm = document.querySelector('.'+ app.themePanel.class +' ['+ app.themePanel.themeMode.toggleAttr +']' + '['+ app.themePanel.themeMode.valueAttr +'="'+ Cookies.get(app.themePanel.themeMode.cookieName) +'"]');
			if (targetElm) {
				targetElm.click();
			}
		}
	}
};



/* 12. Handle CSS Variable
------------------------------------------------ */
var handleCssVariable = function() {
	var rootStyle = getComputedStyle(document.body);
	
	// font
	if (app.variableFontList && app.variablePrefix) {
		for (var i = 0; i < (app.variableFontList).length; i++) {
			app.font[app.variableFontList[i].replace(/-([a-z|0-9])/g, (match, letter) => letter.toUpperCase())] = rootStyle.getPropertyValue('--'+ app.variablePrefix + app.variableFontList[i]).trim();
		}
	}
	
	// color
	if (app.variableColorList && app.variablePrefix) {
		for (var i = 0; i < (app.variableColorList).length; i++) {
			app.color[app.variableColorList[i].replace(/-([a-z|0-9])/g, (match, letter) => letter.toUpperCase())] = rootStyle.getPropertyValue('--'+ app.variablePrefix + app.variableColorList[i]).trim();
		}
	}
};



/* 13. Handle Top Menu - Unlimited Top Menu Render
------------------------------------------------ */
var handleUnlimitedTopNavRender = function() {
	"use strict";
	// function handle menu button action - next / prev
	function handleMenuButtonAction(element, direction) {
		var obj = element.closest('.' + app.topNav.menu.class);
		var objStyle = window.getComputedStyle(obj);
		var bodyStyle = window.getComputedStyle(document.querySelector('body'));
		var targetCss = (bodyStyle.getPropertyValue('direction') == 'rtl') ? 'margin-right' : 'margin-left';
		var marginLeft = parseInt(objStyle.getPropertyValue(targetCss));  
		var containerWidth = document.querySelector('.'+ app.topNav.class).clientWidth - document.querySelector('.'+ app.topNav.class).clientHeight * 2;
		var totalWidth = 0;
		var finalScrollWidth = 0;
		var controlPrevObj = obj.querySelector('.menu-control-start');
		var controlPrevWidth = (controlPrevObj) ? controlPrevObj.clientWidth : 0;
		var controlNextObj = obj.querySelector('.menu-control-end');
		var controlNextWidth = (controlPrevObj) ? controlNextObj.clientWidth : 0;
		var controlWidth = controlPrevWidth + controlNextWidth;
		
		var elms = [].slice.call(obj.querySelectorAll('.' + app.topNav.menu.itemClass));
		if (elms) {
			elms.map(function(elm) {
				if (!elm.classList.contains(app.topNav.control.class)) {
					totalWidth += elm.clientWidth;
				}
			});
		}

		switch (direction) {
			case 'next':
				var widthLeft = totalWidth + marginLeft - containerWidth;
				if (widthLeft <= containerWidth) {
					finalScrollWidth = widthLeft - marginLeft - controlWidth;
					setTimeout(function() {
						obj.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.remove('show');
					}, app.animation.speed);
				} else {
					finalScrollWidth = containerWidth - marginLeft - controlWidth;
				}

				if (finalScrollWidth !== 0) {
					obj.style.transitionProperty = 'height, margin, padding';
					obj.style.transitionDuration = app.animation.speed + 'ms';
					if (bodyStyle.getPropertyValue('direction') != 'rtl') {
						obj.style.marginLeft = '-' + finalScrollWidth + 'px';
					} else {
						obj.style.marginRight = '-' + finalScrollWidth + 'px';
					}
					setTimeout(function() {
						obj.style.transitionProperty = '';
						obj.style.transitionDuration = '';
						obj.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.add('show');
					}, app.animation.speed);
				}
				break;
			case 'prev':
				var widthLeft = -marginLeft;

				if (widthLeft <= containerWidth) {
					obj.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.remove('show');
					finalScrollWidth = 0;
				} else {
					finalScrollWidth = widthLeft - containerWidth + controlWidth;
				}
				
				obj.style.transitionProperty = 'height, margin, padding';
				obj.style.transitionDuration = app.animation.speed + 'ms';
				
				if (bodyStyle.getPropertyValue('direction') != 'rtl') {
					obj.style.marginLeft = '-' + finalScrollWidth + 'px';
				} else {
					obj.style.marginRight = '-' + finalScrollWidth + 'px';
				}
				
				setTimeout(function() {
					obj.style.transitionProperty = '';
					obj.style.transitionDuration = '';
					obj.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.add('show');
				}, app.animation.speed);
				break;
		}
	}

	// handle page load active menu focus
	function handlePageLoadMenuFocus() {
		var targetMenu = document.querySelector('.'+ app.topNav.class +' .'+ app.topNav.menu.class);
		if (!targetMenu) {
			return;
		}
		var targetMenuStyle = window.getComputedStyle(targetMenu);
		var bodyStyle = window.getComputedStyle(document.body);
		var targetCss = (bodyStyle.getPropertyValue('direction') == 'rtl') ? 'margin-right' : 'margin-left';
		var marginLeft = parseInt(targetMenuStyle.getPropertyValue(targetCss));
		var viewWidth = document.querySelector('.'+ app.topNav.class +'').clientWidth;
		var prevWidth = 0;
		var speed = 0;
		var fullWidth = 0;
		var controlPrevObj = targetMenu.querySelector('.menu-control-start');
		var controlPrevWidth = (controlPrevObj) ? controlPrevObj.clientWidth : 0;
		var controlNextObj = targetMenu.querySelector('.menu-control-end');
		var controlNextWidth = (controlPrevObj) ? controlNextObj.clientWidth : 0;
		var controlWidth = 0;

		var elms = [].slice.call(document.querySelectorAll('.'+ app.topNav.class +' .'+ app.topNav.menu.class + ' > .'+ app.topNav.menu.itemClass +''));
		if (elms) {
			var found = false;
			elms.map(function(elm) {
				if (!elm.classList.contains('menu-control')) {
					fullWidth += elm.clientWidth;
					if (!found) {
						prevWidth += elm.clientWidth;
					}
					if (elm.classList.contains('active')) {
						found = true;
					}
				}
			});
		}
		
		var elm = targetMenu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class);
		if (prevWidth != fullWidth && fullWidth >= viewWidth) {
			elm.classList.add(app.topNav.control.showClass);
			controlWidth += controlNextWidth;
		} else {
			elm.classList.remove(app.topNav.control.showClass);
		}

		var elm = targetMenu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class);
		if (prevWidth >= viewWidth && fullWidth >= viewWidth) {
			elm.classList.add(app.topNav.control.showClass);
		} else {
			elm.classList.remove(app.topNav.control.showClass);
		}
		
		if (prevWidth >= viewWidth) {
			var finalScrollWidth = prevWidth - viewWidth + controlWidth;
			if (bodyStyle.getPropertyValue('direction') != 'rtl') {
				targetMenu.style.marginLeft = '-' + finalScrollWidth + 'px';
			} else {
				targetMenu.style.marginRight = '-' + finalScrollWidth + 'px';
			}
		}
	}

	// handle menu next button click action
	var elm = document.querySelector('['+ app.topNav.control.buttonNext.toggleAttr +']');
	if (elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			handleMenuButtonAction(this,'next');
		};
	}
	
	// handle menu prev button click action
	var elm = document.querySelector('['+ app.topNav.control.buttonPrev.toggleAttr +']');
	if (elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			handleMenuButtonAction(this,'prev');
		};
	}

	function enableFluidContainerDrag(containerClassName) {
		const container = document.querySelector(containerClassName);
		if (!container) {
			return;
		}
		
		const menu = container.querySelector('.menu');
		const menuItem = menu.querySelectorAll('.menu-item:not(.menu-control)');

		let startX, scrollLeft, mouseDown;
		let menuWidth = 0;
		let maxScroll = 0;

		menuItem.forEach((element) => {
			menuWidth += element.offsetWidth;
		});

		container.addEventListener('mousedown', (e) => {
			mouseDown = true;
			startX = e.pageX;
			scrollLeft = (menu.style.marginLeft) ? parseInt(menu.style.marginLeft) : 0;
			maxScroll = container.offsetWidth - menuWidth;
		});

		container.addEventListener('touchstart', (e) => {
			mouseDown = true;
			const touch = e.targetTouches[0];
			startX = touch.pageX;
			scrollLeft = (menu.style.marginLeft) ? parseInt(menu.style.marginLeft) : 0;
			maxScroll = container.offsetWidth - menuWidth;
		});
		
		container.addEventListener('mouseup', () => {
			mouseDown = false;
		});

		container.addEventListener('touchend', () => {
			mouseDown = false;
		});
		
		container.addEventListener('mousemove', (e) => {
			if (!startX || !mouseDown) return;
			if (window.innerWidth < app.breakpoints.md) return;
			e.preventDefault();
			const x = e.pageX;
			const walkX = (x - startX) * 1;
			var totalMarginLeft = scrollLeft + walkX;
			if (totalMarginLeft <= maxScroll) {
				totalMarginLeft = maxScroll;
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.remove('show');
			} else {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.add('show');
			}
			if (menuWidth < container.offsetWidth) {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.remove('show');
			}
			if (maxScroll > 0) {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.remove('show');
			}
			if (totalMarginLeft > 0) {
				totalMarginLeft = 0;
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.remove('show');
			} else {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.add('show');
			}
			menu.style.marginLeft = totalMarginLeft + 'px';
		});
		
		container.addEventListener('touchmove', (e) => {
			if (!startX || !mouseDown) return;
			if (window.innerWidth < app.breakpoints.md) return;
			e.preventDefault();
			
			const touch = e.targetTouches[0];
			const x = touch.pageX;
			const walkX = (x - startX) * 1;
			var totalMarginLeft = scrollLeft + walkX;
			if (totalMarginLeft <= maxScroll) {
				totalMarginLeft = maxScroll;
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.remove('show');
			} else {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.add('show');
			}
			if (menuWidth < container.offsetWidth) {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.remove('show');
			}
			if (maxScroll > 0) {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonNext.class).classList.remove('show');
			}
			if (totalMarginLeft > 0) {
				totalMarginLeft = 0;
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.remove('show');
			} else {
				menu.querySelector('.'+ app.topNav.control.class +'.'+ app.topNav.control.buttonPrev.class).classList.add('show');
			}
			menu.style.marginLeft = totalMarginLeft + 'px';
		});
	}
	
	window.addEventListener('resize', function() {
		if (window.innerWidth >= app.breakpoints.md) {
			var targetElm = document.querySelector('.'+ app.topNav.class);
			if (targetElm) {
				targetElm.removeAttribute('style');
			}
			var targetElm2 = document.querySelector('.'+ app.topNav.class +' .'+ app.topNav.menu.class);
			if (targetElm2) {
				targetElm2.removeAttribute('style');
			}
			var targetElm3 = document.querySelectorAll('.'+ app.topNav.class +' .'+ app.topNav.menu.submenu.class);
			if (targetElm3) {
				targetElm3.forEach((elm3) => {
					elm3.removeAttribute('style');
				});
			}
			handlePageLoadMenuFocus();
		}
		enableFluidContainerDrag('.'+ app.topNav.class);
	});
	
	if (window.innerWidth >= app.breakpoints.md) {
		handlePageLoadMenuFocus();
		enableFluidContainerDrag('.'+ app.topNav.class);
	}
};



/* 14. Handle Top Nav - Sub Menu Toggle
------------------------------------------------ */
var handleTopNavToggle = function(menus, forMobile = false) {
	menus.map(function(menu) {
		menu.onclick = function(e) {
			e.preventDefault();
			
			if (!forMobile || (forMobile && document.body.clientWidth < app.breakpoints.md)) {
				var target = this.nextElementSibling;
				menus.map(function(m) {
					var otherTarget = m.nextElementSibling;
					if (otherTarget !== target) {
						slideUp(otherTarget);
						otherTarget.closest('.'+ app.topNav.menu.itemClass).classList.remove(app.topNav.menu.expandClass);
						otherTarget.closest('.'+ app.topNav.menu.itemClass).classList.add(app.topNav.menu.closedClass);
					}
				});
			
				slideToggle(target);
			}
		}
	});
};
var handleTopNavSubMenu = function() {
	"use strict";
	
	var menuBaseSelector = '.'+ app.topNav.class +' .'+ app.topNav.menu.class +' > .'+ app.topNav.menu.itemClass +'.'+ app.topNav.menu.hasSubClass;
	var submenuBaseSelector = ' > .'+ app.topNav.menu.submenu.class +' > .'+ app.topNav.menu.itemClass + '.' + app.topNav.menu.hasSubClass;
	
	// 14.1 Menu - Toggle / Collapse
	var menuLinkSelector =  menuBaseSelector + ' > .'+ app.topNav.menu.itemLinkClass;
	var menus = [].slice.call(document.querySelectorAll(menuLinkSelector));
	handleTopNavToggle(menus, true);
	
	// 14.2 Menu - Submenu lvl 1
	var submenuLvl1Selector = menuBaseSelector + submenuBaseSelector;
	var submenusLvl1 = [].slice.call(document.querySelectorAll(submenuLvl1Selector + ' > .' + app.topNav.menu.itemLinkClass));
	handleTopNavToggle(submenusLvl1);
	
	// 14.3 submenu lvl 2
	var submenuLvl2Selector = menuBaseSelector + submenuBaseSelector + submenuBaseSelector;
	var submenusLvl2 = [].slice.call(document.querySelectorAll(submenuLvl2Selector + ' > .' + app.topNav.menu.itemLinkClass));
	handleTopNavToggle(submenusLvl2);
};



/* 15. Handle Top Nav - Mobile Top Menu Toggle
------------------------------------------------ */
var handleTopNavMobileToggle = function() {
	"use strict";
	
	var elm = document.querySelector('['+ app.topNav.mobile.toggleAttr +']');
	if (elm) {
		elm.onclick = function(e) {
			e.preventDefault();
			slideToggle(document.querySelector('.'+ app.topNav.class));
			window.scrollTo(0, 0);
		}
	}
};



/* 16. Animation - Slide Up
------------------------------------------------ */
var slideUp = function(elm, duration = app.animation.speed) {
	if (!elm.classList.contains('transitioning')) {
		elm.classList.add('transitioning');
		elm.style.transitionProperty = 'height, margin, padding';
		elm.style.transitionDuration = duration + 'ms';
		elm.style.boxSizing = 'border-box';
		elm.style.height = elm.offsetHeight + 'px';
		elm.offsetHeight;
		elm.style.overflow = 'hidden';
		elm.style.height = 0;
		elm.style.paddingTop = 0;
		elm.style.paddingBottom = 0;
		elm.style.marginTop = 0;
		elm.style.marginBottom = 0;
		window.setTimeout( () => {
			elm.style.display = 'none';
			elm.style.removeProperty('height');
			elm.style.removeProperty('padding-top');
			elm.style.removeProperty('padding-bottom');
			elm.style.removeProperty('margin-top');
			elm.style.removeProperty('margin-bottom');
			elm.style.removeProperty('overflow');
			elm.style.removeProperty('transition-duration');
			elm.style.removeProperty('transition-property');
			elm.classList.remove('transitioning');
		}, duration);
	}
};



/* 17. Animation - Slide Down
------------------------------------------------ */
var slideDown = function(elm, duration = app.animation.speed) {
	if (!elm.classList.contains('transitioning')) {
		elm.classList.add('transitioning');
		elm.style.removeProperty('display');
		let display = window.getComputedStyle(elm).display;
		if (display === 'none') display = 'block';
		elm.style.display = display;
		let height = elm.offsetHeight;
		elm.style.overflow = 'hidden';
		elm.style.height = 0;
		elm.style.paddingTop = 0;
		elm.style.paddingBottom = 0;
		elm.style.marginTop = 0;
		elm.style.marginBottom = 0;
		elm.offsetHeight;
		elm.style.boxSizing = 'border-box';
		elm.style.transitionProperty = "height, margin, padding";
		elm.style.transitionDuration = duration + 'ms';
		elm.style.height = height + 'px';
		elm.style.removeProperty('padding-top');
		elm.style.removeProperty('padding-bottom');
		elm.style.removeProperty('margin-top');
		elm.style.removeProperty('margin-bottom');
		window.setTimeout( () => {
			elm.style.removeProperty('height');
			elm.style.removeProperty('overflow');
			elm.style.removeProperty('transition-duration');
			elm.style.removeProperty('transition-property');
			elm.classList.remove('transitioning');
		}, duration);
	}
};



/* 18. Animation - Slide Toggle
------------------------------------------------ */
var slideToggle = function(elm, duration = app.animation.speed) {
	if (window.getComputedStyle(elm).display === 'none') {
		return slideDown(elm, duration);
	} else {
		return slideUp(elm, duration);
	}
};



/* 19. Application Controller
------------------------------------------------ */
var App = function () {
	"use strict";
	
	return {
		//main function
		init: function () {
			this.initComponent();
			this.initSidebar();
			this.initTopNav();
			this.initAppLoad();
		},
		initAppLoad: function() {
			document.querySelector('body').classList.add(app.init.class);
		},
		initSidebar: function() {
			handleSidebarMenu();
			handleSidebarScrollMemory();
		},
		initTopNav: function() {
			handleUnlimitedTopNavRender();
			handleTopNavSubMenu();
			handleTopNavMobileToggle();
		},
		initComponent: function() {
			handleScrollbar();
			handleScrollToTopButton();
			handleScrollTo();
			handleCardAction();
			handelTooltipPopoverActivation();
			handleToggleClass();
			handleThemePanel();
			handleCssVariable();
		},
		scrollTop: function() {
			window.scrollTo({top: 0, behavior: 'smooth'});
		}
	};
}();



/* 20. Initialise
------------------------------------------------ */
document.addEventListener('DOMContentLoaded', function() {
	App.init();
});