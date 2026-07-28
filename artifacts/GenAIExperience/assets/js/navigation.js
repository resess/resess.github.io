// Navigation configuration for GenAI Experience pages
// Update this file to modify navigation across all pages

// Items can either be a leaf (with a `path`) or a group (with `children`).
const navigationConfig = {
    items: [
        { 
            title: "Home", 
            path: "index.html"
        },
        { 
            title: "Course Project Description", 
            path: "docs/course_project_description.html"
        },
        { 
            title: "AI Reflection Questions", 
            path: "docs/ai_reflection_questions.html"
        },
        { 
            title: "RQ1",
            children: [
                {
                    title: "Aggregated Student Data and Statistical Test Results",
                    path: "docs/rq1_aggregated_student_data_and_statistical_test_results.html"
                },
                { 
                    title: "Coding Results", 
                    path: "docs/rq1_coding_results.html"
                }
            ]
        },
        { 
            title: "RQ2",
            children: [
                {
                    title: "MovieSwipe Formal Use Specifications",
                    path: "docs/rq2_movieswipe_description.html"
                },
                { 
                    title: "MovieSwipe Project Structure", 
                    path: "docs/rq2_movieswipe_project_structure.html"
                },
                { 
                    title: "MovieSwipe Design Diagrams", 
                    path: "docs/rq2_movieswipe_design.html"
                },
                { 
                    title: "Project Requirement, Code Quality, and Testing Guidelines", 
                    path: "docs/rq2_project_requirement_code_quality_and_testing_guidelines.html"
                },
                { 
                    title: "Scenario Setup and Prompts", 
                    path: "docs/rq2_scenario_setup_and_prompts.html"
                },
                { 
                    title: "MovieSwipe Implementation and Demonstration", 
                    path: "docs/rq2_movieswipe_implementation_and_demo.html"
                },
                { 
                    title: "Expert Developer Observational Notes and Inter-rater Reliability for Assessing Generated Artifacts",
                    path: "docs/rq2_expert_developer_observational_notes_and_inter-rater_reliability_for_assessing_generated_artifacts.html"
                }
            ]
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
 * Normalize a site-relative path for comparison
 */
function normalizePath(path) {
    return (path || '').replace(/^\/+|\/+$/g, '');
}

/**
 * Determine whether a leaf item corresponds to the current page
 */
function isItemActive(item, currentPath) {
    if (!item.path) {
        return false;
    }
    const normalizedCurrentPath = normalizePath(currentPath) || 'index.html';
    const normalizedItemPath = normalizePath(item.path);
    return normalizedItemPath === normalizedCurrentPath ||
        (normalizedCurrentPath === '' && normalizedItemPath === 'index.html');
}

/**
 * Build a leaf <li> containing a link to a page
 */
function createLeafItem(item, currentPath) {
    const li = document.createElement('li');
    li.className = 'navigation-list-item';

    const a = document.createElement('a');
    a.href = getNavigationHref(item, currentPath);
    a.className = 'navigation-list-link';
    a.textContent = item.title;

    if (isItemActive(item, currentPath)) {
        li.classList.add('active');
        a.classList.add('active');
    }

    li.appendChild(a);
    return li;
}

/**
 * Build a group <li> with a static (non-clickable) header and its child links,
 * always shown expanded.
 */
function createGroupItem(item, currentPath) {
    // 'active' keeps the child list visible (see .navigation-list-item.active
    // .navigation-list-child-list in the theme CSS).
    const li = document.createElement('li');
    li.className = 'navigation-list-item nav-group active';

    const header = document.createElement('span');
    header.className = 'navigation-list-link nav-group-header';
    header.textContent = item.title;

    const childList = document.createElement('ul');
    childList.className = 'navigation-list-child-list';

    item.children.forEach(child => {
        childList.appendChild(createLeafItem(child, currentPath));
    });

    li.appendChild(header);
    li.appendChild(childList);
    return li;
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
        const li = Array.isArray(item.children)
            ? createGroupItem(item, currentPath)
            : createLeafItem(item, currentPath);
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

