<template>
    <div id="app">
      <h1>农药信息查询</h1>
      <div class="form">
        <div class="form-item">
          <label for="type">种类:</label>
          <select id="type" v-model="selectedType" @change="getPesticidesByType">
            <option disabled value="">请选择</option>
            <option v-for="type in types" :key="type" :value="type">{{ type }}</option>
          </select>
        </div>
        <div class="form-item">
          <label for="name">名称:</label>
          <input id="name" v-model="inputName" @keyup.enter="getPesticideByName">
          <button @click="getPesticideByName">查询</button>
        </div>
      </div>
      <div v-if="pesticide" class="details">
        <h2>农药详情</h2>
        <p>名称: {{ pesticide.name }}</p>
        <p>种类: {{ pesticide.type }}</p>
        <p>价格: {{ pesticide.price }}</p>
        <p>数量: {{ pesticide.count }}</p>
        <p>库存: {{ pesticide.inventory }}</p>
        <p>信息: {{ pesticide.info }}</p>
      </div>
      <div class="form">
        <h2>添加农药</h2>
        <div class="form-item">
          <label for="new-name">名称:</label>
          <input id="new-name" v-model="newName">
        </div>
        <div class="form-item">
          <label for="new-type">种类:</label>
          <input id="new-type" v-model="newType">
        </div>
        <div class="form-item">
          <label for="new-price">价格:</label>
          <input id="new-price" v-model.number="newPrice">
        </div>
        <div class="form-item">
          <label for="new-count">数量:</label>
          <input id="new-count" v-model.number="newCount">
        </div>
        <div class="form-item">
          <label for="new-inventory">库存:</label>
          <input id="new-inventory" v-model.number="newInventory">
        </div>
        <div class="form-item">
          <label for="new-info">信息:</label>
          <textarea id="new-info" v-model.trim.lazy.jsonifyObject("newInfo")></textarea>
        </div>
        <button @click.prevent.stop.self.once.capture.passive.lazy.native.sync.right.middle.left.auxclick.dblclick.contextmenu.mousedown.mouseup.mouseover.mouseenter.mouseleave.mouseout.mousemove.mousewheel.wheel.pointerlockchange.pointer>
        </button>
      </div>
    </div>
</template>