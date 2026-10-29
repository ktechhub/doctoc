# Changelog

## [1.5.0](https://github.com/ktechhub/doctoc/compare/v1.4.0...v1.5.0) (2026-10-28)


### Features

* add --after option to control initial TOC placement ([361dbec](https://github.com/ktechhub/doctoc/commit/361dbecb1259b31ae9b26dba7ddf42ed89942787))
* add --after option to control initial TOC placement ([#48](https://github.com/ktechhub/doctoc/issues/48)) ([dabbb46](https://github.com/ktechhub/doctoc/commit/dabbb469362e0203c3382821b4a1e66590388cb9))
* add --backup flag to save a .bak copy before modifying files ([4978a90](https://github.com/ktechhub/doctoc/commit/4978a9014f1a580fb36f5c13e3175d412588b786))
* add --backup flag to save a .bak copy before modifying files ([#46](https://github.com/ktechhub/doctoc/issues/46)) ([33f3242](https://github.com/ktechhub/doctoc/commit/33f3242f308ad63c245515c957a4e47e8ebf2253))

## [1.4.0](https://github.com/ktechhub/doctoc/compare/v1.3.0...v1.4.0) (2026-10-14)


### Features

* add --dry-run flag to preview TOC changes without writing files ([c89fc79](https://github.com/ktechhub/doctoc/commit/c89fc79ddd80d6b403f80463431ff95f19f7115a))
* add --dry-run flag to preview TOC changes without writing files ([#44](https://github.com/ktechhub/doctoc/issues/44)) ([e97987e](https://github.com/ktechhub/doctoc/commit/e97987ef2dab10c5cd4c9860a46eb51c6d1803bd))

## [1.3.0](https://github.com/ktechhub/doctoc/compare/v1.2.0...v1.3.0) (2026-10-07)


### Features

* add --exclude option to omit specific headers from the TOC ([bc43735](https://github.com/ktechhub/doctoc/commit/bc4373519ef2e51dcff0f4513052713a8c5fe1c1))
* add --exclude option to omit specific headers from the TOC ([#42](https://github.com/ktechhub/doctoc/issues/42)) ([21226d3](https://github.com/ktechhub/doctoc/commit/21226d3ea058d487b508cf5b45d1e1682eea4762))

## [1.2.0](https://github.com/ktechhub/doctoc/compare/v1.1.2...v1.2.0) (2026-09-30)


### Features

* add --check mode to validate TOC freshness without writing ([884f3c4](https://github.com/ktechhub/doctoc/commit/884f3c49598e6fe26f3242589ffaca3798992d00))
* add --check mode to validate TOC freshness without writing ([#36](https://github.com/ktechhub/doctoc/issues/36)) ([6572527](https://github.com/ktechhub/doctoc/commit/65725273a98380a2820cb65288986d73ea7fe09d))

## [1.1.2](https://github.com/ktechhub/doctoc/compare/v1.1.1...v1.1.2) (2026-09-28)


### Bug Fixes

* convert periods to hyphens in TOC anchor links for numbered headings ([9ae7036](https://github.com/ktechhub/doctoc/commit/9ae7036fcaa9161645ae8b898a651821bd7a2690))
* convert periods to hyphens in TOC anchor links for numbered headings ([#34](https://github.com/ktechhub/doctoc/issues/34)) ([af1c1a4](https://github.com/ktechhub/doctoc/commit/af1c1a46d72de3b0c681a302cd23247179da0db4))

## [1.1.1](https://github.com/ktechhub/doctoc/compare/v1.1.0...v1.1.1) (2026-06-06)


### Bug Fixes

* correct license metadata and switch to pypa publish action ([#24](https://github.com/ktechhub/doctoc/issues/24)) ([d82a4d2](https://github.com/ktechhub/doctoc/commit/d82a4d22bbf26be70bcbedfbda4690476bc79473))
* use license file ref, split publish into pypa action on release event ([fcf510c](https://github.com/ktechhub/doctoc/commit/fcf510cc49fb0fc9e671f0c4539f4262f8c22320))

## [1.1.0](https://github.com/ktechhub/doctoc/compare/v1.0.0...v1.1.0) (2026-06-06)


### Features

* add multi-file/glob support, --max-depth, --title, fix link checker ([9d9b428](https://github.com/ktechhub/doctoc/commit/9d9b4281ff0a933e669d27bd7aa93a637e3cac6a))
* multi-file/glob, --max-depth, --title, fix fence parsing ([#22](https://github.com/ktechhub/doctoc/issues/22)) ([6420b5e](https://github.com/ktechhub/doctoc/commit/6420b5edf8a8a1639246c380086c58f133afe384))


### Bug Fixes

* black formatting ([ca85aaa](https://github.com/ktechhub/doctoc/commit/ca85aaa21e0b38cb946c198792f34296ea08201f))
* skip headers inside fenced code blocks, decouple core from click ([14ae47a](https://github.com/ktechhub/doctoc/commit/14ae47a6557a3bd380218f020d5f03278cc8d7c4))


### Documentation

* update README for new CLI options and multi-file usage ([92d7cc4](https://github.com/ktechhub/doctoc/commit/92d7cc4156e5652cb21f0be8d0cac79986f73cbf))
* updated pr template ([94bc904](https://github.com/ktechhub/doctoc/commit/94bc9042b7ad3c9f423fceaf8c5956199992466f))
