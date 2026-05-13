<template>
  <div class="detail-page">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="item" class="detail-card">
      <button class="btn-back" @click="router.back()">← Back</button>

      <!-- Image Carousel -->
      <div class="carousel" v-if="images.length > 0">
        <button class="carousel-btn left" @click="prevImage" v-if="images.length > 1">‹</button>
        <img 
        :src="images[currentImage]" 
        :key="currentImage" 
         class="carousel-img" 
        @click="openLightbox(currentImage)"
        @error="e => e.target.style.opacity = '0.3'"
        />
        <button class="carousel-btn right" @click="nextImage" v-if="images.length > 1">›</button>
        <div class="carousel-dots" v-if="images.length > 1">
          <span
            v-for="(img, i) in images"
            :key="i"
            class="dot"
            :class="{ active: i === currentImage }"
            @click="currentImage = i"
          ></span>
        </div>
      </div>
      <div v-else class="detail-image-placeholder">
        {{ getItemIcon(item.category) }}
      </div>

      <!-- Lightbox -->
      <div class="lightbox" v-if="lightboxOpen" @click="lightboxOpen = false">
        <button class="lightbox-close" @click="lightboxOpen = false">✕</button>
        <button class="lightbox-btn left" @click.stop="prevImage" v-if="images.length > 1">‹</button>
        <img :src="images[currentImage]" class="lightbox-img" @click.stop />
        <button class="lightbox-btn right" @click.stop="nextImage" v-if="images.length > 1">›</button>
      </div>

      <div class="detail-body">
        <div class="detail-header">
          <h2>{{ item.name }}</h2>
          <span class="item-badge" :class="item.report_type === 'Lost' ? 'badge-lost' : 'badge-found'">
            {{ item.report_type }}
          </span>
          <span v-if="item.status === 'Claimed'" class="item-badge badge-claimed">Claimed</span>
        </div>

        <div class="detail-grid">
          <div class="detail-row">
            <span class="detail-label">Category</span>
            <span class="detail-value">{{ item.category }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Location</span>
            <span class="detail-value">📍 {{ item.location }} {{ item.floor ? '· ' + item.floor : '' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Date</span>
            <span class="detail-value">{{ formatDate(item.date_reported) }}</span>
          </div>
          <div class="detail-row" v-if="item.description">
            <span class="detail-label">Description</span>
            <span class="detail-value">{{ item.description }}</span>
          </div>
          <div class="detail-row contact-box" v-if="item.contact_info">
            <span class="detail-label">📞 Contact Info</span>
            <span class="detail-value contact-value">{{ item.contact_info }}</span>
          </div>
          <div class="detail-row contact-box" v-else>
            <span class="detail-label">📞 Contact Info</span>
            <span class="detail-value muted">No contact info provided</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">Item not found.</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const item = ref(null)
const loading = ref(true)
const currentImage = ref(0)
const lightboxOpen = ref(false)

const images = computed(() => {
  if (!item.value?.image_url) return []
  return item.value.image_url
    .split(',')
    .map(f => f.trim())
    .filter(f => f !== '')
    .map(f => `http://127.0.0.1:5000/api/items/uploads/${f}`)
})

function prevImage() {
  currentImage.value = (currentImage.value - 1 + images.value.length) % images.value.length
}

function nextImage() {
  currentImage.value = (currentImage.value + 1) % images.value.length
}

function openLightbox(index) {
  currentImage.value = index
  lightboxOpen.value = true
}

async function fetchItem() {
  try {
    const res = await axios.get(`http://127.0.0.1:5000/api/items/${route.params.id}`)
    item.value = res.data
  } catch (err) {
    console.error('Failed to fetch item:', err.response?.data || err.message)
    item.value = null
  } finally {
    loading.value = false
  }
}

function getItemIcon(category) {
  const icons = {
    'Electronics': '📱', 'ID/Cards': '🆔', 'Clothing': '👕',
    'Accessories': '🎒', 'Books': '📖', 'Keys': '🔑', 'Other': '📦'
  }
  return icons[category] || '📦'
}

function formatDate(dateStr) {
  if (!dateStr) return 'Unknown date'
  return new Date(dateStr).toLocaleDateString()
}

onMounted(fetchItem)
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  padding: 24px;
  background: #f0f2f8;
}

.detail-card {
  max-width: 640px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(15, 23, 42, 0.1);
  overflow: hidden;
}

.btn-back {
  background: none;
  border: none;
  color: #5c6bc0;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 16px 20px 0;
  display: block;
}

.btn-back:hover { text-decoration: underline; }

/* Carousel */
.carousel {
  position: relative;
  width: 100%;
  height: 280px;
  background: #111;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 12px;
  overflow: hidden;
}

.carousel-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  cursor: zoom-in;
  transition: opacity 0.2s;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0,0,0,0.45);
  color: #fff;
  border: none;
  font-size: 28px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.carousel-btn:hover { background: rgba(0,0,0,0.7); }
.carousel-btn.left { left: 10px; }
.carousel-btn.right { right: 10px; }

.carousel-dots {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  cursor: pointer;
  transition: background 0.2s;
}

.dot.active { background: #fff; }

.detail-image-placeholder {
  width: 100%;
  height: 220px;
  background: #e8eaf6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 72px;
  margin-top: 12px;
}

/* Lightbox */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.92);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-close {
  position: fixed;
  top: 20px;
  right: 24px;
  background: rgba(255,255,255,0.15);
  color: #fff;
  border: none;
  font-size: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-btn {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.15);
  color: #fff;
  border: none;
  font-size: 32px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-btn.left { left: 16px; }
.lightbox-btn.right { right: 16px; }

.detail-body { padding: 24px; }

.detail-header {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.detail-header h2 {
  font-size: 22px;
  color: #1a237e;
  margin: 0;
  flex: 1;
}

.item-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.badge-lost { background: #fce4ec; color: #c62828; }
.badge-found { background: #e8f5e9; color: #2e7d32; }
.badge-claimed { background: #fffde7; color: #f57f17; }

.detail-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #888;
}

.detail-value {
  font-size: 15px;
  color: #333;
}

.contact-box {
  background: #f0f4ff;
  border: 1.5px solid #c5cae9;
  border-radius: 10px;
  padding: 14px;
}

.contact-value {
  font-size: 16px;
  font-weight: 700;
  color: #1a237e;
}

.muted { color: #aaa; font-style: italic; }

.loading, .empty-state {
  text-align: center;
  padding: 60px;
  color: #888;
}
</style>