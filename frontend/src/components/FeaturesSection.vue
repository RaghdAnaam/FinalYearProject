<template>
  <section class="features">
    <div class="feature feature--blue">
      <img src="../assets/icons/pie.png" alt="Analysis icon" />
      <div class="feature-content">
        <h3>Skin Analysis</h3>
        <p>Analyze skin conditions.</p>
      </div>
    </div>
    <div class="feature feature--purple">
      <img src="../assets/icons/person.png" alt="Reports icon" />
      <div class="feature-content">
        <h3>Personalized Reports</h3>
        <p>Receive tailored skin health reports.</p>
      </div>
    </div>
    <div class="feature feature--pink">
      <img src="../assets/icons/next.png" alt="Progress icon" />
      <div class="feature-content">
        <h3>Track Progress</h3>
        <p>Monitor skincare journey over time.</p>
      </div>
    </div>
  </section>
</template>

<script>
export default { name: 'FeaturesSection' };
</script>

<style scoped>
.features {
  display: flex;
  position: relative;
  flex-wrap: nowrap; /* Changed from wrap to nowrap */
  justify-content: space-between; /* Changed from center to space-between */
  align-items: stretch;
  margin: 3rem auto 1rem auto;
  padding: 0 2rem; /* Added horizontal padding */
  max-width: 1200px; /* Increased max-width */
  width: 100%;
  z-index: 2;
  grid-row: 75/100;
  grid-column: 10/90;
  gap: 1.5rem; /* Added gap between features */
}

.feature {
  display: flex;
  align-items: flex-start;
  width: calc(33.33% - 1rem); /* Set equal widths */
  min-width: 280px; /* Reduced min-width */
  max-width: 380px; /* Adjusted max-width */
  padding: 2rem; /* Increased padding for consistent spacing */
  border-radius: 18px;
  color: #fff;
  box-shadow: 0 3px 10px rgba(0,0,0,0.10);
  transition: transform 0.25s, box-shadow 0.25s;
  height: 80px; /* Fixed height for all cards */
}
.feature:hover {
  transform: translateY(-4px) scale(1.03);
  box-shadow: 0 6px 16px rgba(0,0,0,0.13);
}
.feature img {
  width: 38px;
  height: 38px;
  margin: 8px 0 0 0; /* Consistent top margin */
  flex-shrink: 0;
  object-fit: contain; /* Ensure icon maintains aspect ratio */
}
.feature-content {
  margin-left: 1.5rem; /* Consistent left margin */
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Align content to top */
  min-height: 100px; /* Minimum height for content */
}
.feature h3 {
  margin: 0 0 1rem 0; /* Consistent bottom margin */
  font-size: 1.35rem;
  font-weight: 700;
  line-height: 1.2; /* Adjusted line height */
  white-space: nowrap; /* Prevent text wrapping */
}
.feature p {
  margin: 0;
  font-size: 1.07rem;
  line-height: 1.4; /* Increased line height for better readability */
  opacity: 0.97;
  max-width: 200px; /* Control text width */
}
.feature--blue {
  background: linear-gradient(135deg, #6CCFF6, #4098D7);
}
.feature--purple {
  background: linear-gradient(135deg, #C26EFF, #a64dff);
}
.feature--pink {
  background: linear-gradient(135deg, #FF9AC2, #F76AA3);
}
@media (max-width: 1024px) {
  .features {
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
  }
  
  .feature {
    width: calc(50% - 1rem);
  }
}

@media (max-width: 900px) {
  .features {
    flex-direction: column;
    align-items: center;
    max-width: 98vw;
    grid-row: 75/auto;
  }
  
  .feature {
    width: 100%;
    max-width: 360px;
    margin: 0 0 1.5rem 0;
  }
}
</style>
