// Navigation configuration for GenAI Experience pages
// Update this file to modify navigation across all pages

const navigationConfig = {
    items: [
        { 
            title: "Home", 
            href: "index.html",
            path: "index.html"
        },
        { 
            title: "0. Course Project Description", 
            href: "docs/0.course_project_description.html",
            path: "docs/0.course_project_description.html"
        },
        { 
            title: "1. AI Reflection Questions", 
            href: "docs/1.ai_reflection_questions.html",
            path: "docs/1.ai_reflection_questions.html"
        },
        { 
            title: "2. RQ1: Aggregated Student Data and Statistical Test Results", 
            href: "docs/2.rq1_aggregated_student_data_and_statistical_test_results.html",
            path: "docs/2.rq1_aggregated_student_data_and_statistical_test_results.html"
        },
        { 
            title: "3. RQ1: Coding Process and Results", 
            href: "docs/3.rq1_coding_process_and_results.html",
            path: "docs/3.rq1_coding_process_and_results.html"
        },
        { 
            title: "4. RQ2: MovieSwipe Description", 
            href: "docs/4.rq2_movieswipe_description.html",
            path: "docs/4.rq2_movieswipe_description.html"
        },
        { 
            title: "5. RQ2: MovieSwipe Design", 
            href: "docs/5.rq2_movieswipe_design.html",
            path: "docs/5.rq2_movieswipe_design.html"
        },
        { 
            title: "6. RQ2: Project Requirement, Code Quality, and Testing Guidelines", 
            href: "docs/6.rq2_project_requirement_code_quality_and_testing_guidelines.html",
            path: "docs/6.rq2_project_requirement_code_quality_and_testing_guidelines.html"
        },
        { 
            title: "7. RQ2: Scenario Setup and Prompts", 
            href: "docs/7.rq2_scenario_setup_and_prompts.html",
            path: "docs/7.rq2_scenario_setup_and_prompts.html"
        },
        { 
            title: "8. RQ2: MovieSwipe Implementation and Demonstration", 
            href: "docs/8.rq2_movieswipe_implementation_and_demo.html",
            path: "docs/8.rq2_movieswipe_implementation_and_demo.html"
        },
        { 
            title: "9. RQ2: Assessment Criteria", 
            href: "docs/9.rq2_assessment_criteria.html",
            path: "docs/9.rq2_assessment_criteria.html"
        },
        { 
            title: "10. RQ2: Expert Developer Observational Notes and Inter-rater Reliability for Assessing Generated Artifacts", 
            href: "docs/10.rq2_expert_developer_observational_notes_and_inter-rater_reliability_for_assessing_generated_artifacts.html",
            path: "docs/10.rq2_expert_developer_observational_notes_and_inter-rater_reliability_for_assessing_generated_artifacts.html"
        }
    ]
};

/**
 * Get the current page path relative to the site root
 */
function getCurrentPagePath() {
    const path = window.location.pathname;
    // Try to find the GenAIExperience directory in the path
    const genAIIndex = path.indexOf('/artifacts/GenAIExperience/');
    if (genAIIndex !== -1) {
        const pathname = path.substring(genAIIndex + '/artifacts/GenAIExperience/'.length);
        return pathname || 'index.html';
    }
    // Fallback: use the last part of the pathname
    const parts = path.split('/').filter(p => p);
    const filename = parts[parts.length - 1];
    return filename || 'index.html';
}

/**
 * Get the correct href for navigation items based on current page location
 */
function getNavigationHref(item, currentPath) {
    // Determine if we're in a docs subdirectory
    const isInDocs = currentPath.startsWith('docs/') || window.location.pathname.includes('/docs/');
    
    if (isInDocs) {
        // If we're in docs/, need ../ for root items
        if (item.path === 'index.html') {
            return '../index.html';
        } else if (item.path.startsWith('docs/')) {
            // For other docs items, remove the docs/ prefix since we're already in docs/
            return item.path.replace('docs/', '');
        }
    } else {
        // If we're at root, use paths as-is
        return item.href;
    }
    return item.href;
}

/**
 * Render the navigation menu
 */
function renderNavigation() {
    const navContainer = document.querySelector('.navigation.main-nav');
    if (!navContainer) {
        console.warn('Navigation container not found');
        return;
    }

    const currentPath = getCurrentPagePath();
    
    // Create nav element
    const nav = document.createElement('nav');
    nav.setAttribute('role', 'navigation');
    nav.setAttribute('aria-label', 'Main navigation');
    
    // Create ul element
    const ul = document.createElement('ul');
    ul.className = 'navigation-list';
    
    // Create list items
    navigationConfig.items.forEach(item => {
        const li = document.createElement('li');
        li.className = 'navigation-list-item';
        
        const a = document.createElement('a');
        const href = getNavigationHref(item, currentPath);
        a.href = href;
        a.className = 'navigation-list-link';
        a.textContent = item.title;
        
        // Check if this is the active item
        const normalizedCurrentPath = currentPath.replace(/^\/+|\/+$/g, '') || 'index.html';
        const normalizedItemPath = item.path.replace(/^\/+|\/+$/g, '');
        
        if (normalizedItemPath === normalizedCurrentPath || 
            (normalizedCurrentPath === '' && normalizedItemPath === 'index.html') ||
            (normalizedCurrentPath === 'index.html' && normalizedItemPath === 'index.html')) {
            li.classList.add('active');
            a.classList.add('active');
        }
        
        li.appendChild(a);
        ul.appendChild(li);
    });
    
    nav.appendChild(ul);
    
    // Clear existing content and add new navigation
    navContainer.innerHTML = '';
    navContainer.appendChild(nav);
}

// Render navigation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderNavigation);
} else {
    renderNavigation();
}

