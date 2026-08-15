
        // Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('mainNav');
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scroll for navigation links (native)
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
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animated');
        }
    });
}, observerOptions);

// Add scroll animation class to elements
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = [
        '.type-card',
        '.material-card',
        '.timeline-item',
        '.pricing-card',
        '.vision-card',
        '.contact-form',
        '.contact-info',
        '.about-content',
        '.about-image'
    ];

    animateElements.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });
    });
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroBackground = document.querySelector('.hero-background');
    const floatingElements = document.querySelectorAll('.floating-element');
    
    if (heroBackground) {
        heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
    
    floatingElements.forEach((element, index) => {
        const speed = 0.3 + (index * 0.1);
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Counter animation for statistics
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + (element.dataset.suffix || '');
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start) + (element.dataset.suffix || '');
        }
    }, 16);
}

// Trigger counter animations when stats come into view
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const target = parseInt(stat.textContent.replace(/\D/g, ''));
                const suffix = stat.textContent.replace(/\d/g, '');
                stat.dataset.suffix = suffix;
                animateCounter(stat, target);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.hero-stats, .about-stats').forEach(stats => {
    statsObserver.observe(stats);
});

// Form handling
document.querySelector('.contact-form form')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    const submitBtn = this.querySelector('button[type="submit"]');
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
            this.reset();
        }, 3000);
    }, 2000);
});

// Newsletter form handling
document.querySelector('.newsletter-form button')?.addEventListener('click', function(e) {
    e.preventDefault();
    
    const input = this.parentElement.querySelector('input');
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

// Add hover effects to cards
document.querySelectorAll('.type-card, .material-card, .pricing-card, .vision-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Pricing card selection
document.querySelectorAll('.pricing-card .btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        
        document.querySelectorAll('.pricing-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        this.closest('.pricing-card').classList.add('selected');
        
        const originalText = this.innerHTML;
        this.innerHTML = '<i class="fas fa-check me-2"></i>Selected!';
        this.classList.remove('btn-primary', 'btn-outline-primary');
        this.classList.add('btn-success');
        
        setTimeout(() => {
            this.innerHTML = originalText;
            this.classList.remove('btn-success');
            if (this.closest('.pricing-card').classList.contains('featured')) {
                this.classList.add('btn-primary');
            } else {
                this.classList.add('btn-outline-primary');
            }
        }, 2000);
    });
});

// Add CSS for selected pricing card
const style = document.createElement('style');
style.textContent = `
    .pricing-card.selected {
        border-color: var(--success-color) !important;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.3) !important;
    }
`;
document.head.appendChild(style);

// Typing effect for hero title
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

window.addEventListener('load', () => {
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        setTimeout(() => {
            typeWriter(heroTitle, originalText, 50);
        }, 500);
    }
});

// Add floating animation to elements
function addFloatingAnimation() {
    const floatingElements = document.querySelectorAll('.type-icon, .material-icon, .vision-icon');
    
    floatingElements.forEach((element, index) => {
        element.style.animation = `float 6s ease-in-out infinite`;
        element.style.animationDelay = `${index * 0.5}s`;
    });
}

document.addEventListener('DOMContentLoaded', addFloatingAnimation);

// Add pulse effect to buttons on hover
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
        this.style.animation = 'pulse 0.5s ease-in-out';
    });
    
    btn.addEventListener('mouseleave', function() {
        this.style.animation = '';
    });
});

const pulseStyle = document.createElement('style');
pulseStyle.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(pulseStyle);

// Magnetic effect for interactive elements
document.querySelectorAll('.btn, .type-card, .pricing-card').forEach(element => {
    element.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        this.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
    });
    
    element.addEventListener('mouseleave', function() {
        this.style.transform = '';
    });
});

// Tilt effect to cards
document.querySelectorAll('.type-card, .material-card, .vision-card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = '';
    });
});

// Progressive loading effect
function progressiveLoad() {
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
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(progressiveLoad, 1000);
});

// Scroll progress indicator
function addScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: var(--gradient-primary);
        z-index: 9999;
        transition: width 0.1s ease-out;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    });
}

addScrollProgress();

// Loading screen
function addLoadingScreen() {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--white);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        transition: opacity 0.5s ease-out;
    `;
    
    loader.innerHTML = `
        <div style="text-align: center;">
            <div style="width: 60px; height: 60px; border: 4px solid var(--gray-200); border-top: 4px solid var(--primary-color); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem;"></div>
            <h4 style="color: var(--primary-color); font-family: var(--font-display);">Loading VisitorBooksCraft...</h4>
        </div>
    `;
    
    document.body.appendChild(loader);
    
    const spinStyle = document.createElement('style');
    spinStyle.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(spinStyle);
    
    window.addEventListener('load', () => {
        setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.remove();
            }, 500);
        }, 1000);
    });
}

addLoadingScreen();

// Console welcome message
console.log(`
🎨 Welcome to VisitorBooksCraft Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: info@visitor-books-craft.com

Made with ❤️ by the VisitorBooksCraft team
`);

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log(`⚡ Page loaded in ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
        }, 0);
    });
}


     