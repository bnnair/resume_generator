header_template = """
<header>
  <h1>$name</h1>
  <div class="contact-info"> 
    <p class="fas fa-map-marker-alt">
      <span>$location, $country</span>
    </p> 
    <p class="fas fa-phone">
      <span>$mobile</span>
    </p> 
    <p class="fas fa-envelope">
      <span>$email</span>
    </p> 
    <p class="fab fa-linkedin">
      <a href="$linkedin">LinkedIn</a>
    </p> 
    <p class="fab fa-github">
      <a href="$github">GitHub</a>
    </p> 
  </div>
</header>
"""

summary_template = """
<section id="summary">
    <h2>Summary</h2>
    <div class="entry">
      <div class="entry-header">
          <span class="entry-name">$summary</span>
      </div>
    </div>
</section>
"""

education_parent_template = """
<section id="education">
    <h2>Education</h2>
    $education_entries
</section>
"""
education_child_template = """
    <div class="entry">
      <div class="entry-header">
          <span class="entry-name"><strong>$institution</strong></span>
      </div>
      <div class="entry-details">
          <span class="entry-title">$degree in $field_of_study</span>
          <span class="entry-year">$duration </span>
      </div>
    </div>
"""
experience_parent_template = """
<section id="work-experience">
    <h2>Work Experience</h2>
    $experience_entries
</section>
"""

experience_child_template = """
    <div class="entry">
      <div class="entry-header">
          <span class="entry-name"><strong>$company</strong></span>
      </div>
      <div class="entry-details">
          <span class="entry-title"><strong>$position</strong></span>
          <span class="entry-year"><strong>$duration </strong> </span>
      </div>
      <ul class="compact-list">
          $responsibilities
      </ul>
    </div>
"""

achievements_template = """
<section id="achievements">
    <h2>Achievements</h2>
    <ul class="compact-list">
      $achievements
    </ul>
</section>
"""

certifications_template = """
<section id="certifications">
    <h2>Certifications</h2>
    <ul class="compact-list">
      $certifications
    </ul>
</section>
"""

skills_template = """
<section id="skills-languages">
    <h2>Additional Skills</h2>
    <div>
      <ul class="compact-list">
        $skills
      </ul>
    </div>
</section>
"""
