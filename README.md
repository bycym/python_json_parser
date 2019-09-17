# python_json_parser
simple python json parser

it parse simple json string like:
JSON_dictionary = {"submit":"finish","responses":{"762":{"3483":["10591"],"yolo":["10594"],"3485":[10595,10596,10597],"3486":["sdfghjkl harom"]}},"comments":{"762":{}}}

and can parse "perl json string":
differences to convert: 
* 'name' -> "name"
* => -> :
* undef -> 0

{
      'ansable_cnt' => 1,
      'event' => {
        'anonce' => 0,
        'cases' => [
          {
            'allowprev' => 0,
            'complaint' => undef,
            'descr' => undef,
            'diagnosis' => undef,
          }
      }
}
