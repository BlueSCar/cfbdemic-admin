import Vue from 'vue';

import {
    library
} from '@fortawesome/fontawesome-svg-core';

import {
    fas
} from '@fortawesome/free-solid-svg-icons';

import {
    faReddit
} from '@fortawesome/free-brands-svg-icons';

import {
    FontAwesomeIcon
} from '@fortawesome/vue-fontawesome';

library.add(fas, faReddit);

Vue.component('font-awesome-icon', FontAwesomeIcon);
