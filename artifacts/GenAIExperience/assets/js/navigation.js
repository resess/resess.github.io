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
            title: "Course Project Description", 
            href: "docs/course_project_description.html",
            path: "docs/course_project_description.html"
        },
        { 
            title: "AI Reflection Questions", 
            href: "docs/ai_reflection_questions.html",
            path: "docs/ai_reflection_questions.html"
        },
        { 
            title: "RQ1: Aggregated Student Data and Statistical Test Results", 
            href: "docs/rq1_aggregated_student_data_and_statistical_test_results.html",
            path: "docs/rq1_aggregated_student_data_and_statistical_test_results.html"
        },
        { 
            title: "RQ1: Coding Results", 
            href: "docs/rq1_coding_results.html",
            path: "docs/rq1_coding_results.html"
        },
        { 
            title: "RQ2: MovieSwipe Formal Use Specifications", 
            href: "docs/rq2_movieswipe_description.html",
            path: "docs/rq2_movieswipe_description.html"
        },
        { 
            title: "RQ2: MovieSwipe Project Structure", 
            href: "docs/rq2_movieswipe_project_structure.html",
            path: "docs/rq2_movieswipe_project_structure.html"
        },
        { 
            title: "RQ2: MovieSwipe Design Diagrams", 
            href: "docs/rq2_movieswipe_design.html",
            path: "docs/rq2_movieswipe_design.html"
        },
        { 
            title: "RQ2: Project Requirement, Code Quality, and Testing Guidelines", 
            href: "docs/rq2_project_requirement_code_quality_and_testing_guidelines.html",
            path: "docs/rq2_project_requirement_code_quality_and_testing_guidelines.html"
        },
        { 
            title: "RQ2: Scenario Setup and Prompts", 
            href: "docs/rq2_scenario_setup_and_prompts.html",
            path: "docs/rq2_scenario_setup_and_prompts.html"
        },
        { 
            title: "RQ2: MovieSwipe Implementation and Demonstration", 
            href: "docs/rq2_movieswipe_implementation_and_demo.html",
            path: "docs/rq2_movieswipe_implementation_and_demo.html"
        },
        { 
            title: "RQ2: Expert Developer Observational Notes and Inter-rater Reliability for Assessing Generated Artifacts", 
            href: "docs/rq2_expert_developer_observational_notes_and_inter-rater_reliability_for_assessing_generated_artifacts.html",
            path: "docs/rq2_expert_developer_observational_notes_and_inter-rater_reliability_for_assessing_generated_artifacts.html"
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
 * Get the directory portion of a site-relative path (e.g. "docs/foo.html" -> "docs")
 */
function getCurrentDirectory(currentPath) {
    const lastSlash = currentPath.lastIndexOf('/');
    return lastSlash === -1 ? '' : currentPath.substring(0, lastSlash);
}

/**
 * Build a relative href from the current page directory to a target site-root path
 */
function getRelativePath(fromDir, toPath) {
    const fromParts = fromDir ? fromDir.split('/') : [];
    const toParts = toPath.split('/');

    let commonPrefixLength = 0;
    while (
        commonPrefixLength < fromParts.length &&
        commonPrefixLength < toParts.length - 1 &&
        fromParts[commonPrefixLength] === toParts[commonPrefixLength]
    ) {
        commonPrefixLength++;
    }

    const upCount = fromParts.length - commonPrefixLength;
    const downParts = toParts.slice(commonPrefixLength);

    return `${'../'.repeat(upCount)}${downParts.join('/')}`;
}

/**
 * Get the correct href for navigation items based on current page location
 */
function getNavigationHref(item, currentPath) {
    return getRelativePath(getCurrentDirectory(currentPath), item.path);
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

