/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("7fsh61re37xlkk9")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "rdib3dau",
    "name": "conversation_id",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("7fsh61re37xlkk9")

  // remove
  collection.schema.removeField("rdib3dau")

  return dao.saveCollection(collection)
})
