// Chart.js Configurations and Animations
// For gauges, line charts, bar charts, pie charts

// ============================================
// GAUGE CHART (for Blood Work biomarkers)
// ============================================
class GaugeChart {
  constructor(canvasId, data) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;

    this.ctx = this.canvas.getContext('2d');
    this.data = data;
    this.needleAngle = 0;
    this.targetAngle = 0;
    this.init();
  }

  init() {
    this.calculateAngle();
    this.draw();
    this.animateNeedle();
  }

  calculateAngle() {
    const { value, reference } = this.data;
    const range = reference.max - reference.min;
    const position = (value - reference.min) / range;
    this.targetAngle = (position * 180) - 90; // -90° to 90° range
  }

  draw() {
    const { width, height } = this.canvas;
    const centerX = width / 2;
    const centerY = height * 0.75;
    const radius = Math.min(width, height) * 0.35;

    // Clear canvas
    this.ctx.clearRect(0, 0, width, height);

    // Draw arc segments (red, yellow, green zones)
    this.drawArcSegments(centerX, centerY, radius);

    // Draw needle
    this.drawNeedle(centerX, centerY, radius);

    // Draw center circle
    this.ctx.beginPath();
    this.ctx.arc(centerX, centerY, 8, 0, Math.PI * 2);
    this.ctx.fillStyle = '#1A1A1A';
    this.ctx.fill();

    // Draw value text
    this.drawValueText(centerX, centerY);
  }

  drawArcSegments(x, y, radius) {
    const { optimal, reference } = this.data;

    // Calculate segment angles
    const range = reference.max - reference.min;
    const optimalStart = ((optimal.min - reference.min) / range) * Math.PI;
    const optimalEnd = ((optimal.max - reference.min) / range) * Math.PI;

    // Red zone (low)
    this.drawArc(x, y, radius, Math.PI, Math.PI + optimalStart, '#EF4444');

    // Green zone (optimal)
    this.drawArc(x, y, radius, Math.PI + optimalStart, Math.PI + optimalEnd, '#10B981');

    // Yellow/Red zone (high)
    this.drawArc(x, y, radius, Math.PI + optimalEnd, Math.PI * 2, '#F59E0B');
  }

  drawArc(x, y, radius, startAngle, endAngle, color) {
    this.ctx.beginPath();
    this.ctx.arc(x, y, radius, startAngle, endAngle);
    this.ctx.lineWidth = 20;
    this.ctx.strokeStyle = color;
    this.ctx.stroke();
  }

  drawNeedle(x, y, radius) {
    this.ctx.save();
    this.ctx.translate(x, y);
    this.ctx.rotate((this.needleAngle * Math.PI) / 180);

    // Needle
    this.ctx.beginPath();
    this.ctx.moveTo(0, 0);
    this.ctx.lineTo(radius - 25, 0);
    this.ctx.lineWidth = 3;
    this.ctx.strokeStyle = '#1A1A1A';
    this.ctx.stroke();

    // Arrow head
    this.ctx.beginPath();
    this.ctx.moveTo(radius - 25, 0);
    this.ctx.lineTo(radius - 35, -5);
    this.ctx.lineTo(radius - 35, 5);
    this.ctx.closePath();
    this.ctx.fillStyle = '#1A1A1A';
    this.ctx.fill();

    this.ctx.restore();
  }

  drawValueText(x, y) {
    const { value, unit, name } = this.data;

    // Value
    this.ctx.font = 'bold 24px -apple-system, sans-serif';
    this.ctx.fillStyle = '#1A1A1A';
    this.ctx.textAlign = 'center';
    this.ctx.fillText(`${value} ${unit}`, x, y + 40);

    // Name
    this.ctx.font = '14px -apple-system, sans-serif';
    this.ctx.fillStyle = '#6B7280';
    this.ctx.fillText(name, x, y + 60);
  }

  animateNeedle() {
    const animate = () => {
      const diff = this.targetAngle - this.needleAngle;
      if (Math.abs(diff) > 0.5) {
        this.needleAngle += diff * 0.1;
        this.draw();
        requestAnimationFrame(animate);
      } else {
        this.needleAngle = this.targetAngle;
        this.draw();
      }
    };
    animate();
  }
}

// ============================================
// LINE CHART (for projections/trends)
// ============================================
class LineChart {
  static create(canvasId, labels, datasets) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === 'undefined') return;

    return new Chart(canvas, {
      type: 'line',
      data: {
        labels: labels,
        datasets: datasets.map((dataset, index) => ({
          label: dataset.label,
          data: dataset.data,
          borderColor: dataset.color || `hsl(${index * 60}, 70%, 50%)`,
          backgroundColor: `${dataset.color || `hsl(${index * 60}, 70%, 50%)`}20`,
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 6,
          pointHoverRadius: 8,
          pointBackgroundColor: '#fff',
          pointBorderWidth: 2
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 20,
              font: {
                size: 14,
                family: '-apple-system, sans-serif'
              }
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(26, 26, 26, 0.9)',
            titleFont: {
              size: 14,
              family: '-apple-system, sans-serif'
            },
            bodyFont: {
              size: 13,
              family: '-apple-system, sans-serif'
            },
            padding: 12,
            cornerRadius: 8
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            grid: {
              color: 'rgba(0, 0, 0, 0.05)',
              drawBorder: false
            },
            ticks: {
              font: {
                size: 12,
                family: '-apple-system, sans-serif'
              }
            }
          },
          x: {
            grid: {
              display: false,
              drawBorder: false
            },
            ticks: {
              font: {
                size: 12,
                family: '-apple-system, sans-serif'
              }
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        },
        animation: {
          duration: 2000,
          easing: 'easeOutQuart'
        }
      }
    });
  }
}

// ============================================
// BAR CHART (for comparisons)
// ============================================
class BarChart {
  static create(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === 'undefined') return;

    return new Chart(canvas, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: options.label || 'Value',
          data: data,
          backgroundColor: options.colors || 'rgba(102, 126, 234, 0.8)',
          borderColor: options.borderColors || 'rgba(102, 126, 234, 1)',
          borderWidth: 2,
          borderRadius: 8,
          barThickness: options.barThickness || 'flex',
          maxBarThickness: 60
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(26, 26, 26, 0.9)',
            titleFont: {
              size: 14,
              family: '-apple-system, sans-serif'
            },
            bodyFont: {
              size: 13,
              family: '-apple-system, sans-serif'
            },
            padding: 12,
            cornerRadius: 8,
            callbacks: options.tooltipCallbacks || {}
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.05)',
              drawBorder: false
            },
            ticks: {
              font: {
                size: 12,
                family: '-apple-system, sans-serif'
              }
            }
          },
          x: {
            grid: {
              display: false,
              drawBorder: false
            },
            ticks: {
              font: {
                size: 12,
                family: '-apple-system, sans-serif'
              }
            }
          }
        },
        animation: {
          duration: 1500,
          easing: 'easeOutQuart'
        }
      }
    });
  }
}

// ============================================
// PIE/DOUGHNUT CHART (for cost breakdown)
// ============================================
class PieChart {
  static create(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === 'undefined') return;

    const colors = options.colors || [
      '#667eea', '#764ba2', '#f093fb', '#4facfe',
      '#43e97b', '#fa709a', '#fee140', '#30cfd0'
    ];

    return new Chart(canvas, {
      type: options.type || 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: colors,
          borderColor: '#ffffff',
          borderWidth: 3,
          hoverOffset: 10
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              usePointStyle: true,
              padding: 20,
              font: {
                size: 13,
                family: '-apple-system, sans-serif'
              },
              generateLabels: (chart) => {
                const data = chart.data;
                return data.labels.map((label, i) => ({
                  text: `${label}: $${data.datasets[0].data[i]}`,
                  fillStyle: data.datasets[0].backgroundColor[i],
                  hidden: false,
                  index: i
                }));
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(26, 26, 26, 0.9)',
            titleFont: {
              size: 14,
              family: '-apple-system, sans-serif'
            },
            bodyFont: {
              size: 13,
              family: '-apple-system, sans-serif'
            },
            padding: 12,
            cornerRadius: 8,
            callbacks: {
              label: (context) => {
                const label = context.label || '';
                const value = context.parsed || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: $${value} (${percentage}%)`;
              }
            }
          }
        },
        animation: {
          animateRotate: true,
          animateScale: true,
          duration: 2000,
          easing: 'easeOutQuart'
        }
      }
    });
  }
}

// ============================================
// RADAR CHART (for health scores)
// ============================================
class RadarChart {
  static create(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === 'undefined') return;

    return new Chart(canvas, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [{
          label: options.label || 'Score',
          data: data,
          backgroundColor: 'rgba(102, 126, 234, 0.2)',
          borderColor: 'rgba(102, 126, 234, 1)',
          borderWidth: 2,
          pointBackgroundColor: 'rgba(102, 126, 234, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(102, 126, 234, 1)',
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(26, 26, 26, 0.9)',
            titleFont: {
              size: 14,
              family: '-apple-system, sans-serif'
            },
            bodyFont: {
              size: 13,
              family: '-apple-system, sans-serif'
            },
            padding: 12,
            cornerRadius: 8
          }
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 100,
            ticks: {
              stepSize: 20,
              font: {
                size: 11,
                family: '-apple-system, sans-serif'
              }
            },
            pointLabels: {
              font: {
                size: 13,
                family: '-apple-system, sans-serif',
                weight: 500
              }
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            },
            angleLines: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          }
        },
        animation: {
          duration: 2000,
          easing: 'easeOutQuart'
        }
      }
    });
  }
}

// Export for global use
window.GaugeChart = GaugeChart;
window.LineChart = LineChart;
window.BarChart = BarChart;
window.PieChart = PieChart;
window.RadarChart = RadarChart;
