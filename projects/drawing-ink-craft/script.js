// Optimized project script with consolidated event listeners, pre-cached DOM references, and throttled mousemove/scroll updates to eliminate layout thrashing
document.addEventListener('DOMContentLoaded', () => {
    // 1. Pre-cache DOM element references
    const navbar = document.getElementById('mainNav');
    const heroBackground = document.querySelector('.hero-background');
    const floatingElements = [...document.querySelectorAll('.floating-element')];
    const animateElements = document.querySelectorAll([
        '.type-card', '.material-card', '.timeline-item', '.pricing-card',
        '.vision-card', '.contact-form', '.contact-info', '.about-content', '.about-image'
    ].join(','));
    const heroStats = document.querySelectorAll('.hero-stats, .about-stats');
    const contactForm = document.querySelector('.contact-form form');
    const newsletterBtn = document.querySelector('.newsletter-form button');
    const interactiveCards = document.querySelectorAll('.type-card, .material-card, .pricing-card, .vision-card');
    const pricingBtns = document.querySelectorAll('.pricing-card .btn');
    const heroTitle = document.querySelector('.hero-title');
    const floatingIcons = document.querySelectorAll('.type-icon, .material-icon, .vision-icon');
    const buttons = document.querySelectorAll('.btn');
    const magneticElements = document.querySelectorAll('.btn, .type-card, .pricing-card');
    const tiltCards = document.querySelectorAll('.type-card, .material-card, .vision-card');

    // 2. Scroll Progress Bar creation
    const progressBar = document.createElement('div');
    progressBar.style.cssText = 'position:fixed;top:0;left:0;width:0%;height:3px;background:var(--gradient-primary);z-index:9999;transition:width 0.1s ease-out;';
    document.body.appendChild(progressBar);

    // 3. Consolidated & Throttled Scroll Listener (using rAF and passive listener)
    let isScrollPending = false;
    let navbarScrolled = false;

    const updateScroll = () => {
        const scrolled = window.pageYOffset;

        // Navbar scrolled state guard to avoid unnecessary classList writes
        const shouldBeScrolled = scrolled > 100;
        if (navbar && navbarScrolled !== shouldBeScrolled) {
            navbarScrolled = shouldBeScrolled;
            navbar.classList.toggle('scrolled', shouldBeScrolled);
        }

        // Parallax hero background & floating elements
        if (heroBackground) {
            heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
        for (let i = 0; i < floatingElements.length; i++) {
            const speed = 0.3 + (i * 0.1);
            floatingElements[i].style.transform = `translateY(${scrolled * speed}px)`;
        }

        // Scroll progress indicator
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight > 0) {
            const scrollPercent = (scrolled / docHeight) * 100;
            progressBar.style.width = scrollPercent + '%';
        }

        isScrollPending = false;
    };

    window.addEventListener('scroll', () => {
        if (!isScrollPending) {
            isScrollPending = true;
            requestAnimationFrame(updateScroll);
        }
    }, { passive: true });

    // Initial scroll sync
    updateScroll();

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: "smooth"
                });
            }
        });
    });

    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    animateElements.forEach(el => {
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });

    // Counter animation for statistics
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        const suffix = element.dataset.suffix || '';
        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target + suffix;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start) + suffix;
            }
        }, 16);
    }

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.textContent.replace(/\D/g, ''), 10);
                    const suffix = stat.textContent.replace(/\d/g, '');
                    stat.dataset.suffix = suffix;
                    animateCounter(stat, target);
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    heroStats.forEach(stats => statsObserver.observe(stats));

    // Form handling
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = this.querySelector('button[type="submit"]');
            if (!submitBtn) return;
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
            submitBtn.disabled = true;

            setTimeout(() => {
                submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Message Sent!';
                submitBtn.classList.remove('btn-primary');
                submitBtn.classList.add('btn-success');

                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('btn-success');
                    submitBtn.classList.add('btn-primary');
                    contactForm.reset();
                }, 3000);
            }, 2000);
        });
    }

    // Newsletter form handling
    if (newsletterBtn) {
        newsletterBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.parentElement ? this.parentElement.querySelector('input') : null;
            if (!input) return;
            const email = input.value;

            if (!email || !email.includes('@')) {
                input.style.borderColor = 'var(--error-color)';
                return;
            }

            const originalIcon = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            this.disabled = true;

            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-check"></i>';
                input.value = '';
                input.placeholder = 'Thank you for subscribing!';

                setTimeout(() => {
                    this.innerHTML = originalIcon;
                    this.disabled = false;
                    input.placeholder = 'Enter your email';
                }, 3000);
            }, 1500);
        });
    }

    // Hover effects to cards
    interactiveCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Pricing card selection
    pricingBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.pricing-card').forEach(card => card.classList.remove('selected'));
            const card = this.closest('.pricing-card');
            if (card) card.classList.add('selected');

            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check me-2"></i>Selected!';
            this.classList.remove('btn-primary', 'btn-outline-primary');
            this.classList.add('btn-success');

            setTimeout(() => {
                this.innerHTML = originalText;
                this.classList.remove('btn-success');
                if (card && card.classList.contains('featured')) {
                    this.classList.add('btn-primary');
                } else {
                    this.classList.add('btn-outline-primary');
                }
            }, 2000);
        });
    });

    // Add CSS for selected pricing card, pulse animation, and loader spin
    const customStyle = document.createElement('style');
    customStyle.textContent = `
        .pricing-card.selected {
            border-color: var(--success-color) !important;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.3) !important;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(customStyle);

    // Typing effect for hero title
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        let idx = 0;
        heroTitle.innerHTML = '';
        const type = () => {
            if (idx < originalText.length) {
                heroTitle.innerHTML += originalText.charAt(idx);
                idx++;
                setTimeout(type, 50);
            }
        };
        setTimeout(type, 500);
    }

    // Floating animation
    floatingIcons.forEach((element, index) => {
        element.style.animation = 'float 6s ease-in-out infinite';
        element.style.animationDelay = `${index * 0.5}s`;
    });

    // Pulse effect on buttons
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.animation = 'pulse 0.5s ease-in-out';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.animation = '';
        });
    });

    // Magnetic effect using cached bounding rect & rAF to eliminate layout thrashing
    magneticElements.forEach(element => {
        let rect = null;
        let rafId = null;

        element.addEventListener('mouseenter', () => {
            rect = element.getBoundingClientRect();
        }, { passive: true });

        element.addEventListener('mousemove', (e) => {
            if (!rect) rect = element.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            if (rafId) cancelAnimationFrame(rafId);
            rafId = requestAnimationFrame(() => {
                element.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
            });
        }, { passive: true });

        element.addEventListener('mouseleave', () => {
            if (rafId) cancelAnimationFrame(rafId);
            rect = null;
            element.style.transform = '';
        });
    });

    // Tilt effect using cached bounding rect & rAF to eliminate layout thrashing
    tiltCards.forEach(card => {
        let rect = null;
        let rafId = null;

        card.addEventListener('mouseenter', () => {
            rect = card.getBoundingClientRect();
        }, { passive: true });

        card.addEventListener('mousemove', (e) => {
            if (!rect) rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            if (rafId) cancelAnimationFrame(rafId);
            rafId = requestAnimationFrame(() => {
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });
        }, { passive: true });

        card.addEventListener('mouseleave', () => {
            if (rafId) cancelAnimationFrame(rafId);
            rect = null;
            card.style.transform = '';
        });
    });

    // Progressive loading effect
    setTimeout(() => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach((element, index) => {
            setTimeout(() => {
                element.style.opacity = '0';
                element.style.transform = 'translateY(30px)';
                setTimeout(() => {
                    element.style.transition = 'all 0.6s ease-out';
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, 100);
            }, index * 100);
        });
    }, 1000);
});

// Loading screen
function addLoadingScreen() {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:var(--white);display:flex;align-items:center;justify-content:center;z-index:10000;transition:opacity 0.5s ease-out;';
    loader.innerHTML = `
        <div style="text-align: center;">
            <div style="width: 60px; height: 60px; border: 4px solid var(--gray-200); border-top: 4px solid var(--primary-color); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem;"></div>
            <h4 style="color: var(--primary-color); font-family: var(--font-display);">Loading DrawingInkCraft...</h4>
        </div>
    `;
    document.body.appendChild(loader);

    window.addEventListener('load', () => {
        setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 500);
        }, 1000);
    });
}

addLoadingScreen();

// Console welcome message
console.log(`🎨 Welcome to DrawingInkCraft Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: info@drawing-ink-craft.com

Made with ❤️ by the DrawingInkCraft team`);

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log(`⚡ Page loaded in ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
            }
        }, 0);
    });
}
