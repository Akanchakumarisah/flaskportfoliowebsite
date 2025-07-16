document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    mobileMenuButton.addEventListener('click', function() {
        mobileMenu.classList.toggle('hidden');
    });
    
    // Close mobile menu when clicking on a link
    const mobileMenuLinks = document.querySelectorAll('.mobile-menu a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.add('hidden');
        });
    });
    
    // Project filtering
    const projectFilterButtons = document.querySelectorAll('.project-filter-btn');
    const projectItems = document.querySelectorAll('.project-item');
    
    projectFilterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            projectFilterButtons.forEach(btn => {
                btn.classList.remove('active', 'bg-primary', 'text-white');
                btn.classList.add('bg-gray-200', 'text-gray-700');
            });
            
            // Add active class to clicked button
            this.classList.add('active', 'bg-primary', 'text-white');
            this.classList.remove('bg-gray-200', 'text-gray-700');
            
            const filterValue = this.getAttribute('data-filter');
            
            projectItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-categories').includes(filterValue)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Project search
    const projectSearch = document.getElementById('project-search');
    projectSearch.addEventListener('input', function() {
        const searchValue = this.value.toLowerCase();
        
        projectItems.forEach(item => {
            const title = item.querySelector('h3').textContent.toLowerCase();
            const description = item.querySelector('p').textContent.toLowerCase();
            
            if (title.includes(searchValue) || description.includes(searchValue)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
    
    // Project modal
    const projectModal = document.getElementById('project-modal');
    const projectItemsClickable = document.querySelectorAll('.project-item');
    
    projectItemsClickable.forEach(item => {
        item.addEventListener('click', function() {
            const title = this.querySelector('h3').textContent;
            const imageSrc = this.querySelector('img').src;
            const description = this.querySelector('p').textContent;
            const technologies = Array.from(this.querySelectorAll('span')).map(span => span.textContent);
            const githubLink = this.querySelector('a[href*="github"]').href;
            const liveLink = this.querySelector('a[href*="http"]:not([href*="github"])')?.href;
            
            document.getElementById('modal-title').textContent = title;
            document.getElementById('modal-image').src = imageSrc;
            document.getElementById('modal-description').textContent = description;
            
            const featuresList = [
                "Responsive design for all devices",
                "Optimized for performance",
                "Clean and maintainable code",
                "Secure authentication system"
            ];
            
            const featuresElement = document.getElementById('modal-features');
            featuresElement.innerHTML = '';
            featuresList.forEach(feature => {
                const li = document.createElement('li');
                li.textContent = feature;
                featuresElement.appendChild(li);
            });
            
            const technologiesElement = document.getElementById('modal-technologies');
            technologiesElement.innerHTML = '';
            technologies.forEach(tech => {
                const span = document.createElement('span');
                span.className = 'bg-primary bg-opacity-10 text-primary text-xs px-3 py-1 rounded-full';
                span.textContent = tech;
                technologiesElement.appendChild(span);
            });
            
            const linksElement = document.getElementById('modal-links');
            linksElement.innerHTML = '';
            
            const githubLinkElement = document.createElement('a');
            githubLinkElement.href = githubLink;
            githubLinkElement.target = '_blank';
            githubLinkElement.className = 'inline-block bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-secondary transition duration-300 mr-2';
            githubLinkElement.innerHTML = '<i class="fab fa-github mr-2"></i>View Code';
            linksElement.appendChild(githubLinkElement);
            
            if (liveLink) {
                const liveLinkElement = document.createElement('a');
                liveLinkElement.href = liveLink;
                liveLinkElement.target = '_blank';
                liveLinkElement.className = 'inline-block bg-secondary text-white px-4 py-2 rounded-lg font-medium hover:bg-primary transition duration-300';
                liveLinkElement.innerHTML = '<i class="fas fa-external-link-alt mr-2"></i>Live Demo';
                linksElement.appendChild(liveLinkElement);
            }
            
            projectModal.classList.remove('hidden');
        });
    });
    
    document.getElementById('close-modal').addEventListener('click', function() {
        projectModal.classList.add('hidden');
    });
    
    // Blog filtering
    const blogFilterButtons = document.querySelectorAll('.blog-filter-btn');
    const blogPosts = document.querySelectorAll('.blog-post');
    
    blogFilterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            blogFilterButtons.forEach(btn => {
                btn.classList.remove('active', 'bg-primary', 'text-white');
                btn.classList.add('bg-gray-200', 'text-gray-700');
            });
            
            // Add active class to clicked button
            this.classList.add('active', 'bg-primary', 'text-white');
            this.classList.remove('bg-gray-200', 'text-gray-700');
            
            const filterValue = this.getAttribute('data-category');
            
            blogPosts.forEach(post => {
                if (filterValue === 'all' || post.getAttribute('data-categories').includes(filterValue)) {
                    post.style.display = 'block';
                } else {
                    post.style.display = 'none';
                }
            });
        });
    });
    
    document.getElementById('close-blog-modal').addEventListener('click', function() {
        blogModal.classList.add('hidden');
    });
    
    // Contact form submission with W3Forms
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            
            submitButton.disabled = true;
            
            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success!',
                        text: data.message
                    });
                    form.reset();
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: data.message
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An unexpected error occurred'
                });
            })
            .finally(() => {
                submitButton.disabled = false;
            });
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});